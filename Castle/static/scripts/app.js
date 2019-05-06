function allowNumbersOnly(e) {
	var code = (e.which) ? e.which : e.keyCode;
	if (code > 31 && (code < 48 || code > 57)) {
			e.preventDefault();
	}
}

$(document).ready(function(){
	
	String.prototype.numberize = function() {
			var target = this;
			return Number(target.split('.').join(''));
	};

	Number.prototype.dotSeperator = function() {
			var target = this;
			return Number(target).toLocaleString('de')
	}


	// $('#price-range-submit').hide();


	$("#min_price,#max_price").on("paste keyup change", function () {                                        
		console.log('new search')

		// var min_price_range = parseInt($("#min_price").val())
		// var max_price_range = parseInt($("#max_price").val());
		var min_price_range = $('#min_price').val().numberize()
		var max_price_range = $('#max_price').val().numberize()
		
		if(max_price_range < min_price_range || isNaN(min_price_range) || isNaN(max_price_range)) {
			$('#slider-range').css('background', 'gray')
			$('#submitFormButton').prop('disabled', true)
		} else {
			$('#slider-range').css('background', '#5e1d1d')
			$('#submitFormButton').prop('disabled', false)
		}
		$("#slider-range").slider({
			values: [$('#min_price').val().numberize(), $('#max_price').val().numberize()]
			// values: [$('#min_price').val(), $('#max_price').val()]
		});

	});

	$("#clearFormButton").on('click', (e) => {
		$('#min_price').val('20.000.000')
		$('#max_price').val('90.000.000')
		$('#slider-range').css('background', '#5e1d1d')	
		$("#slider-range").slider({
			values: [20000000, 90000000]
		});
		$('#submitFormButton').prop('disabled', false)
		e.preventDefault()
	})
	


	$(function () {
		$("#slider-range").slider({
		range: true,
		orientation: "horizontal",
		min: 0,
		max: 200000000,
		values: [20000000, 90000000],
		step: 100000,

		slide: function (event, ui) {
			if (ui.values[0] == ui.values[1]) {
				return false;
			}

			$("#min_price").val(Number(ui.values[0]).dotSeperator());
			$("#max_price").val(Number(ui.values[1]).dotSeperator());
			// var min_price_range = parseInt($("#min_price").val())
			// var min_price_range = parseInt($("#min_price").val())
			var min_price_range = $('#min_price').val().numberize();
			var max_price_range = $('#max_price').val().numberize();
			
			if(max_price_range < min_price_range || isNaN(min_price_range) || isNaN(max_price_range)) {
				$('#slider-range').css('background', 'gray')
				$('#submitFormButton').prop('disabled', true)
			} else {
				$('#slider-range').css('background', '#5e1d1d')
				$('#submitFormButton').prop('disabled', false)
			}
		}
		});

		$("#min_price").val(Number($("#slider-range").slider("values", 0)).dotSeperator());
		$("#max_price").val(Number($("#slider-range").slider("values", 1)).dotSeperator());

		// $("#max_price").val(Number($("#max_price").val()).toLocaleString('de'));

	});

	$("#slider-range").click(function () {

		console.log($("#min_price").val().numberize())
		console.log($("#max_price").val().numberize())
	});

	$('#search_zip').on('click', (e) => {
		e.preventDefault()
		e.stopPropagation()
		$('#chooseZIP').modal('show');
	})


	$('i[id^="open_"').on('click', (e) => {
		if($(e.target).attr('class') === 'fas fa-plus-square') {
			$(e.target).attr('class', 'fas fa-minus-square')
			$('.'+$(e.target).data('area')).css('display', 'block')
			$('#'+$(e.target).data('all')).css('display', 'inline')
		} else {
			$(e.target).attr('class', 'fas fa-plus-square')
			$('.'+$(e.target).data('area')).css('display', 'none')
			$('#'+$(e.target).data('all')).css('display', 'none')
		}
	})

	$('a[id^="choose_all_"').on('click', (e) => {
		$('.'+$(e.target).data('area')+ ' input').prop('checked', true);
	})

	//clear all checkboxes
	$('#clear_zip_query').on('click', (e) => {
		$('.item .zip_option input').prop('checked', false)
	})

});
