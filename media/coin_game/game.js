var TR;
TR = {
    getURLParameter: function(sParam) {
        var sPageURL = window.location.search.substring(1);
        var sURLVariables = sPageURL.split('&');
        for (var i = 0; i < sURLVariables.length; i++) {
            var sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] == sParam) {
                return sParameterName[1];
            }
        }
    },
    Coin: function(coinType, index) {
        this.coinType = coinType;
        this.index = index;
        this.status = 'inactive';
        this.values = {
            quarter: 0.25,
            dime: 0.10,
            nickel: 0.05,
            penny: 0.01
        };

        this.selector = coinType + '-' + index;
        this.coinTemplate  = {
            quarter: '<div id="' + this.selector +
                '" class="coin quarter"><div class="handle">+</div>' +
                '<div class="val">25&cent;</div></div>',
            dime: '<div id="' + this.selector +
                '" class="coin dime"><div class="handle">+</div>' +
                '<div class="val">10&cent;</div></div>',
            nickel: '<div id="' + this.selector +
                '" class="coin nickel"><div class="handle">+</div>' +
                '<div class="val">5&cent;</div></div>',
            penny: '<div id="' + this.selector +
                '" class="coin penny"><div class="handle">+</div>' +
                '<div class="val">1&cent;</div></div>'
        };

        this.setValue = function(coinType) {
            this.value = this.values[coinType];
        };
        this.setHtml = function(coinType) {
            this.html = this.coinTemplate[coinType];
            this.appendToBox(this.html);
        };
        this.appendToBox = function(html) {
            $('#' + this.coinType + '-box').append(html);
            $('#' + this.selector).css({
                marginLeft: (this.index * 5) + 'px'
            }).children('.handle').text('+');

            var cssSelector = '#' + this.coinType + '-box .handle';
            $(cssSelector).css({display: 'none'});
            $(cssSelector + ':last').css({
                display: 'block'});
            $('#' + this.selector).click(function() {
                var c = TR.gameInstance.getCoinInstance($(this));
                var cssSelector = '#' + c.coinType + '-box .handle';
                $(this).remove();
                c.appendToGameBoard(c.html, c.selector);
                $('#' + c.selector + ' .handle').css({
                    display: 'block'});
                $(cssSelector).css({display: 'none'});
                $(cssSelector + ':last').css({
                    display: 'block'});
                c.status = 'active';
            });
        };

        this.appendToGameBoard = function(html, selector) {
            $('.board-row-two .board-col-two').append(html);
            var c;
            var elm;
            elm = $('#' + selector);
            c = TR.gameInstance.getCoinInstance($(html));
            elm.css({
                position: 'relative',
                float: 'left',
                marginLeft: (c.index * 8) + 'px'
            }).children('.handle').text('-');

            $(elm).click(function() {
                $(this).remove();
                c.status = 'inactive';
                var cssSelector = '#' + c.coinType + '-box .handle';
                $(cssSelector).css({display: 'none'});
                $(cssSelector + ':last').css({
                    display: 'block'});

                c.appendToBox(c.html);
            });
        };

        this.init = function() {
            this.setValue(this.coinType);
            this.setHtml(this.coinType);
        };

        this.init();
    },

    Board: function(game) {
        this.game = game;
        this.templates = {
            boardArea: function() { return $('<div id="board-area"/>');},
            boardRowOne: function() {
                return $('<div class="board-row-one"/>');},
            boardRowTwo: function() {
                return $('<div class="board-row-two"/>');},
            boardRowThree: function() {
                return $('<div class="board-row-three"/>');},
            boardColOne: function() {
                return $('<div class="board-col-one"/>');},
            boardColTwo: function() {
                return $('<div class="board-col-two"/>');},
            qBox: function() { return $('<div id="quarter-box"/>');},
            dBox: function() { return $('<div id="dime-box"/>');},
            nBox: function() { return $('<div id="nickel-box"/>');},
            pBox: function() { return $('<div id="penny-box"/>');},
            roundBox: function() { return $('<div id="round-box"/>');},
            calcBox: function() {
                var a = $('<div id="calc-box"/>');
                var b = $('<div class="button btn-primary" ' +
                          'id="count-button">Count My Change</div>');
                a.append(b);
                return a;
            }
        };

        this.setBoard = function(selector) {

            this.templates.boardParent = $(selector);
            var t = this.templates;

            var ba = new t.boardArea();
            var bro = new t.boardRowOne();
            var brtw = new t.boardRowTwo();
            var brth = new t.boardRowThree();
            var brcolOneA = new t.boardColOne();
            var brcolOneB = new t.boardColOne();
            var brcolOneC = new t.boardColOne();
            var brcolTwoA = new t.boardColTwo();
            var brcolTwoB = new t.boardColTwo();
            var brcolTwoC = new t.boardColTwo();
            var qBox = new t.qBox();
            var dBox = new t.dBox();
            var nBox = new t.nBox();
            var pBox = new t.pBox();
            var rBox = new t.roundBox();
            var cBox = new t.calcBox();

            t.boardParent.append(ba);
            ba.append(bro);
            ba.append(brtw);
            ba.append(brth);
            brcolOneA.append(rBox);
            brcolOneB.append(qBox, dBox, nBox, pBox);
            bro.append(brcolOneA);
            bro.append(brcolTwoA);
            brtw.append(brcolOneB);
            brtw.append(brcolTwoB);
            brth.append(brcolOneC);
            brth.append(brcolTwoC);
            brcolTwoC.append(cBox);

            //now that board is set add change area
            this.addChangeArea();

            //show the current round
            this.showRound();

            //assign click handler to calcBox
            cBox.click(function() {
                game.calculateRound();
            });
        };
        this.addChangeArea = function() {
            var changeArea = new TR.ChangeArea();
            TR.gameInstance.changeArea = changeArea;
        };

        this.showRound = function(changeArea) {
            var g = TR.gameInstance;
            var text = g.roundText[g.round];
            $('#round-box').empty();
            $('#round-box').text(text);

            if (changeArea) {
                changeArea.showChangeText();
            }
        };
    },
    ChangeArea: function() {
        this.template = $('<div id=\"change-area\">' +
                          '<div class=\"change-header\">' +
                          '</div><div class=\"num-display\"></div></div>');
        this.templateText = {
            1: '$0.87',
            2: '$1.33',
            'header': 'Make This Amount of Change:'
        };
        this.appendToGameBoard = function() {

            $('.board-row-one .board-col-two').append(this.template);
            this.showChangeText();
        };
        this.showChangeText = function() {
            var t = this.template;
            var round = TR.gameInstance.round;
            t.children('.change-header').empty()
                .append(this.templateText.header);
            t.children('.num-display').empty()
                .append(this.templateText[round]);
        };
        this.init = function() {
            this.appendToGameBoard();
        };
        this.init();
    },
    Game: function(selector, round) {
        if (selector === null) {
            if (console) {
                console.log('we need a selector for the game to show up in!');
            }
            return;
        }
        this.status = 'incomplete';
        this.selector = selector;
        this.round = round === '' ? 1 : round;
        this.roundText = {
            1: 'Round 1 of 2',
            2: 'Round 2 of 2'
        };
        this.roundAnswer = {
            1: 0.87,
            2: 1.33
        };
        // make a reference
        TR.gameInstance = this;
        // the game setup
        // setup the number of coins you want
        this.coins = {};
        this.coinSetup = {
            quarter: 5,
            dime: 5,
            nickel: 5,
            penny: 5
        };

        this.gameBoard = new TR.Board(this);
        // make coins
        this.makeCoins = function() {
            var i;
            var c;
            $.each(this.coinSetup, function(key, value) {
                for (i = 0; i < value; i++) {
                    c = new TR.Coin(key, i);
                    TR.gameInstance.coins[c.selector] = c;
                }
            });
        };
        this.getCoinInstance = function(elm) {
            var id = elm.attr('id');
            return TR.gameInstance.coins[id];
        };
        this.calculateChange = function() {
            var coins = this.coins;
            coins.active = [];
            coins.changeCount = 0;
            $.each(coins, function(key, value) {
                if (value.status === 'active') {
                    coins.active.push(this);
                    coins.changeCount += this.value;
                }
            });
            return Math.round(coins.changeCount * 100) / 100;
        };
        this.calculateRound = function() {
            var change = this.calculateChange();
            var answer = this.roundAnswer[this.round];
            var submit = $('#submit');
            if (change === answer && this.round == 2) {
                this.status = 'complete';
            } else if (change === answer) {
                $.post();
                this.status = 'complete';
            }

            if (this.round >= 2 && change !== answer) {
                this.status = 'default';
            }

            this.round++;
            this.alertBox();
        };

        this.updateRound = function() {
            var g = TR.gameInstance;
            $('.coin').remove();
            g.makeCoins();
            g.changeArea.showChangeText();
            g.gameBoard.showRound();

        };

        this.alertBox = function() {
            var status = TR.gameInstance.status;

            var boxTemplate = $('<div id="alert-box" class="' +
                                status + '"></div>');
            var boxText = {
                'incomplete': $('<div class="alert-text"><p>Sorry</p>' +
                                '<p>Sorry, let\'s go to round 2 and ' +
                                'try again!</p></div>'),
                'complete': $('<div class="alert-text"><p>Correct!</p>' +
                              '<p>Nice work! Let\'s move on.</p></div>'),
                'default': $('<div class="alert-text"><p>Sorry, incorect.</p>' +
                             '<p>Let\'s move on anyway.</p></div>')
            };
            var boxBtn = {
                'incomplete': $('<button type="button">Try Again</button/>'),
                'complete': $('<button type="button">Continue</button/>'),
                'default': $('<button type="button">Continue</button/>')
            };
            boxBtn.incomplete.click(function() {
                var g = TR.gameInstance;
                g.updateRound();
                boxTemplate.remove();
                $('#calc-box').show();
            });
            boxBtn.complete.click(function() {
                var g = TR.gameInstance;
                var submit = $('#submit')
                    .length > 0 ? $('#submit') : $('.next a').attr('href');
                if (g.round > 2 && g.status !== 'incomplete') {
                    if (submit.length < 2) {
                        submit.trigger('click');
                    } else {
                        window.location = submit;
                    }
                }
                g.updateRound();
                if (TR.getURLParameter('r') === undefined && g.round === 2) {
                    var winHref = window.location.href + '?r=2';
                    window.location = winHref;
                }
                boxTemplate.remove();
                $('#calc-box').show();
            });
            boxBtn.default.click(function() {
                var g = TR.gameInstance;
                var submit = $('#submit')
                    .length > 0 ? $('#submit') : $('.next a').attr('href');

                if (g.round > 2 && g.status !== 'incomplete') {
                    if (submit.length < 2) {
                        submit.trigger('click');
                    } else {
                        window.location = submit;
                    }
                }
                g.updateRound();
                boxTemplate.remove();
            });
            $('#calc-box').hide();
            boxTemplate.append(boxText[status]);
            boxTemplate.append(boxBtn[status]);
            $(this.selector).append(boxTemplate);
        };
        this.init = function(selector) {
            this.gameBoard.setBoard(selector);
            this.makeCoins();
        };
        this.init(selector);
    }
};
