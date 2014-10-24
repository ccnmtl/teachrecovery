
TR = {
	Coin: function(coinType, index){
		this.coinType = coinType;
		this.index = index;
		this.status = 'inactive';
		this.values = {
			quarter: .25,
			dime: .10,
			nickel: .05,
			penny: .01
		},
		this.selector = coinType + '-' + index;
		this.coinTemplate  = {
				quarter: '<div id="'+ this.selector +'" class="coin quarter"><div class="val">25&cent;</div></div>',
				dime: '<div id="'+ this.selector +'" class="coin dime"><div class="val">10&cent;</div></div>',
				nickel: '<div id="'+ this.selector +'" class="coin nickel"><div class="val">5&cent;</div></div>',
				penny: '<div id="'+ this.selector +'" class="coin penny"><div class="val">1&cent;</div></div>',
		},

		this.setValue = function(coinType){
			this.value = this.values[coinType];
		}
		this.setHtml = function(coinType){
			this.html = this.coinTemplate[coinType];
			this.appendToBox(this.html);
		}
		this.appendToBox = function(html){
			$('#'+this.coinType + '-box').append(html);
			$('#'+this.selector).css({
				marginLeft: (this.index * 5) + 'px'
			})
			$('#'+this.selector).click(function(){
				var coin = $(this).clone();
				$(this).remove();
				c = TR.gameInstance.get_coin_instance($(this));
				c.appendToGameBoard(c.html, c.selector)
				c.status = 'active';
			})
		}
		
		this.appendToGameBoard = function(html, selector){
			$('.board-row-two .board-col-two').append(html);
			var elm = $('#'+selector);
			var c = TR.gameInstance.get_coin_instance($(html));
			elm.css({
				position:'relative',
				float: 'left',
				marginLeft: (c.index *8) + 'px'
			})
			

			$(elm).click(function(){
				$(this).remove();
				var c = TR.gameInstance.get_coin_instance($(this));
				c.appendToBox(c.html)
			})
		}

		this.init = function(){
			this.setValue(this.coinType);
			this.setHtml(this.coinType);
		}

		this.init()
	},

	Board: function(game){
		this.game = game;
		this.templates={
			boardArea : function(){ return $('<div id="board-area"/>')},
			boardRowOne: function(){ return $('<div class="board-row-one"/>')},
			boardRowTwo : function(){ return $('<div class="board-row-two"/>')},
			boardRowThree : function(){ return $('<div class="board-row-three"/>')},
			boardColOne : function(){ return $('<div class="board-col-one"/>')},
			boardColTwo : function(){ return $('<div class="board-col-two"/>')},
			qBox :function(){ return $('<div id="quarter-box"/>')},
			dBox :function(){ return $('<div id="dime-box"/>')},
			nBox :function(){ return $('<div id="nickel-box"/>')},
			pBox :function(){ return $('<div id="penny-box"/>')},
			roundBox :function(){ return $('<div id="round-box"/>')}
		}
		
		this.setBoard = function(selector){

			this.templates.boardParent= $(selector);
			var t = this.templates;
			
			//	just going to set a bunch of global stuff
			// for accessibility
			ba = new t.boardArea();
			bro = new t.boardRowOne();
			brtw = new t.boardRowTwo();
			brth = new t.boardRowThree();
			brcolOneA = new t.boardColOne();
			brcolOneB = new t.boardColOne();
			brcolOneC = new t.boardColOne();
			brcolTwoA = new t.boardColTwo();
			brcolTwoB = new t.boardColTwo();
			brcolTwoC = new t.boardColTwo();
			qBox = new t.qBox();
			dBox = new t.dBox();
			nBox = new t.nBox();
			pBox = new t.pBox();
			rBox = new t.roundBox();

			t.boardParent.append( ba);
			ba.append( bro );
			ba.append( brtw );
			ba.append( brth );
			brcolOneA.append(rBox);
			brcolOneB.append(qBox, dBox, nBox, pBox);
			bro.append(brcolOneA );
			bro.append(brcolTwoA );
			brtw.append(brcolOneB);
			brtw.append(brcolTwoB );
			brth.append(brcolOneC);
			brth.append(brcolTwoC );

			//now that board is set add change area
			this.addChangeArea();

			//show the current round
			this.showRound();
		}
		
		this.addChangeArea = function(){
			var changeArea= new TR.ChangeArea();
			TR.gameInstance.changeArea = changeArea;	
		}

		this.showRound = function(changeArea){
				var g = TR.gameInstance;
				var text = g.roundText[g.round];
				$('#round-box').empty();
				$('#round-box').text(text);

				if(changeArea){
					changeArea.showChangeText()
				}

			}
		
	},
	ChangeArea: function(){
		this.template = $('<div id="change-area"><div class="change-header">\
			</div><div class="num-display"></div></div>');
		this.templateText = {
			1: '$0.87',
			2: '$1.33',
			'header': 'Make This Amount of Change:'
		}
		this.appendToGameBoard = function(){

			$('.board-row-one .board-col-two').append(this.template);
			this.showChangeText();
		}
		this.showChangeText = function(){
						var t = this.template;
			var round = TR.gameInstance.round;
			t.children('.change-header').empty()
				.append(this.templateText['header']);
			t.children('.num-display').empty()
				.append(this.templateText[round]);
		}
		this.init = function(){
			this.appendToGameBoard();
		}
		this.init();
	},
	Game: function(){
		this.round = 1;
		this.roundText = {
			1: "Round 1 of 1",
			2: "Round 1 of 2"
		};
		this.roundAnswer = {
			1: 0.87,
			2: 1.33
		}
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
		}

		this.gameBoard = new TR.Board(this);
		// make coins
		this.makeCoins = function(){
			$.each(this.coinSetup, function(key, value){
				for(i=0;i<value;i++){
					var c = new TR.Coin(key, i);
					TR.gameInstance.coins[c.selector]=c;
				}
			})
		}
		this.get_coin_instance = function(elm){
			var id = elm.attr('id');
			return TR.gameInstance.coins[id];
		}
		this.calculateChange = function(){
			var coins = this.coins;
			coins.active = [];
			coins.changeCount = 0;
			$.each(coins, function(key, value){
				if(value.status == 'active'){
					coins.active.push(this);
					coins.changeCount += this.value;
				}
			})
			return coins.changeCount;
		}
		this.init = function(){
			this.gameBoard.setBoard('body');
			this.makeCoins();
		}
		this.init()
	}
}
jQuery(document).ready(function(){
	(function($) {
		g = new TR.Game();

	})(jQuery);
})

