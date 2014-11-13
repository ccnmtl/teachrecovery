// create a js file to capture how we want to display stuff after submission
jQuery(document).ready(function(){
	window.TR = function(){
		this.calculate_score = function(){
			var answer_vals = this.get_answers_vals();
			var total_answers = answer_vals.correct + answer_vals.wrong;
			var score = answer_vals.correct / total_answers;
			score = Math.ceil(score * 100);
			return score;
		};
		this.get_answers_vals = function(){
			var answer_elms = jQuery('.is-correct');
			var answer_vals = {correct: 0, wrong: 0};
			var correct;
			var wrong; 
			answer_elms.each(function(){
				
				if(jQuery(this).text() == 'False'){
					answer_vals.wrong += 1;
				}
				if(jQuery(this).text() == 'True'){
					answer_vals.correct += 1;
				}
			});
			return answer_vals;
		};
		this.show_feedback = function(tr){
			if (this.calculate_score() > 80){
				this.show_pass_feedback();
			}else{
				this.show_fail_feedback(tr);
			}

			this.show_score();
		};
		this.show_pass_feedback = function(){
			jQuery('#feedback .pass').css({
				display: 'block'
			});
		};
		this.show_fail_feedback = function(tr){
			var weakness_elm = jQuery('#feedback .weakness');
			var weaknesses = this.get_subject_weakness();
			jQuery(weaknesses).each(function(){
				weakness_elm.append('<div class="subject"><p>' + tr.subject_ref[this] + '</p></div>');
			});
			weakness_elm.css({
				display: 'block'
			});
			jQuery('#feedback .fail').css({
				display: 'block'
			});
		};
		this.get_subject_weakness = function(){
			var wrong_answers = jQuery('.is-correct.False');
			var subject_ref = {};
			var subjects = [];
			wrong_answers.each(function(){
				var s = jQuery(this).parent().children('li.quiz-type').text();
				var ref  = jQuery(this).parent().children('li.quiz-description').text();
				subject_ref[s] = ref;
				subjects.push(s);
			});
			this.subject_ref = subject_ref;
			return jQuery.unique(subjects);
		};
		this.show_score = function(){
			var score = this.calculate_score();
			var pass = 'fail';
			if(score > 79){
				pass = 'pass';
			}
			jQuery('#score .percentage').addClass(pass).append(score + '%');
		};
	};


	window.tr = new window.TR();
	window.tr.show_feedback(window.tr);

});
