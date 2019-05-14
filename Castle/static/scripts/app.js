var zipCodes = []
var apartments = []


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


	$('#search_zip').on('mousedown', function(e) {
		e.preventDefault();
		this.blur();
		window.focus();
	});

	// $('#search_rooms').on('click', (e) => {
	// 	$(e.target).hide()
	// 	$("#choose_rooms").show()
	// })

	$('.zip_option').on('click', (e) => {
		zipCodes = $('.zip_option input:checked')
		$('#howManyZips').text(zipCodes.length + ' zip code/s')
	})

	// $('#price-range-submit').hide();


	$("#min_price,#max_price").on("paste keyup change", function (e) {                                        
		console.log('new search', e)

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
	
		$(e.target).val(Number(e.target.value.numberize()).dotSeperator())

	});

	$("#min_size,#max_size").on("paste keyup change", function (e) {                                        
		console.log('new search', e)

		var min_size_range = $('#min_size').val().numberize()
		var max_size_range = $('#max_size').val().numberize()
		
		if(max_size_range < min_size_range || isNaN(min_size_range) || isNaN(max_size_range)) {
			$('#size-range').css('background', 'gray')
			$('#submitFormButton').prop('disabled', true)
		} else {
			$('#size-range').css('background', '#5e1d1d')
			$('#submitFormButton').prop('disabled', false)
		}
		$("#size-range").slider({
			values: [$('#min_size').val().numberize(), $('#max_size').val().numberize()]
		});
	
		$(e.target).val(Number(e.target.value.numberize()).dotSeperator())

	});

	$("#clearFormButton").on('click', (e) => {
		$('#min_price').val('20.000.000')
		$('#max_price').val('90.000.000')
		$('#min_size').val('40')
		$('#max_size').val('250')
		$('#slider-range').css('background', '#5e1d1d')	
		$("#slider-range").slider({
			values: [20000000, 90000000]
		});
		$('#size-range').css('background', '#5e1d1d')	
		$("#size-range").slider({
			values: [40, 250]
		});
		$('#submitFormButton').prop('disabled', false)
		$('#search_rooms').val('Rooms')
		$('#search_address').val('')
		$('.item .zip_option input').prop('checked', false)
		zipCodes = []
		$('#howManyZips').text('Zip codes')
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
		$("#size-range").slider({
		range: true,
		orientation: "horizontal",
		min: 0,
		max: 500,
		values: [40, 250],
		step: 5,

		slide: function (event, ui) {
			if (ui.values[0] == ui.values[1]) {
				return false;
			}

			$("#min_size").val(Number(ui.values[0]).dotSeperator());
			$("#max_size").val(Number(ui.values[1]).dotSeperator());
			// var min_size_range = parseInt($("#min_size").val())
			// var min_size_range = parseInt($("#min_size").val())
			var min_size_range = $('#min_size').val().numberize();
			var max_size_range = $('#max_size').val().numberize();
			
			if(max_size_range < min_size_range || isNaN(min_size_range) || isNaN(max_size_range)) {
				$('#size-range').css('background', 'gray')
				$('#submitFormButton').prop('disabled', true)
			} else {
				$('#size-range').css('background', '#5e1d1d')
				$('#submitFormButton').prop('disabled', false)
			}
		}
		});

		$("#min_price").val(Number($("#slider-range").slider("values", 0)).dotSeperator());
		$("#max_price").val(Number($("#slider-range").slider("values", 1)).dotSeperator());

		$("#min_size").val(Number($("#size-range").slider("values", 0)).dotSeperator());
		$("#max_size").val(Number($("#size-range").slider("values", 1)).dotSeperator());

		// $("#max_price").val(Number($("#max_price").val()).toLocaleString('de'));

	});

	$("#slider-range").click(function () {

		console.log($("#min_price").val().numberize())
		console.log($("#max_price").val().numberize())
	});

	$("#size-range").click(function () {

		console.log($("#min_size").val().numberize())
		console.log($("#max_size").val().numberize())
	});

	$('#search_zip').on('click', (e) => {
		e.preventDefault()
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
		zipCodes = $('.zip_option input:checked')
		$('#howManyZips').text(zipCodes.length + ' zip code/s')
	})

	//clear all checkboxes
	$('#clear_zip_query').on('click', (e) => {
		$('.item .zip_option input').prop('checked', false)
		zipCodes = []
		$('#howManyZips').text('Zip codes')
	})


	$('#submitFormButton').on('click', (e) => {
		e.preventDefault()
		var searchText = $('#search_address').val()
		var minPrice = $("#min_price").val().numberize()
		var maxPrice = $("#max_price").val().numberize()
		var minSize = $('#min_size').val()
		var maxSize = $('#max_size').val()
		var rooms = $('#search_rooms').val()
		if(rooms == '6+') {
			rooms = '6'
		}
		var checked = $('.zip_option input:checked')
		zipcodes = $.map(checked, (input) => {
			return input.value
		})
		$.ajax({
			url: '/apartments?search_filter=' + searchText + '&min_price=' + minPrice + '&max_price=' + maxPrice + '&min_size=' + minSize + '&max_size=' + maxSize + '&rooms=' + rooms + '&zipcodes=' + zipcodes.join(','),
			type: 'GET',
			success: function(res) {
				res = res.map(item => {
					item = item.fields
					return item
				})
				res = {'data': res}
				var newHTML = res.data.map(apartment => {
					return `
						<div data-address="${ apartment.address }" data-price="${ apartment.price }" class="col-md-4 col-lg-3 col-12 col-sm-6 single-apartment" style="padding:1rem">
            				<div class="gray-background border-shadow">
								<div class="card bg-custom border-shadow text-white">
									<a href="${ apartment.id }"><img class="card-img-top" src="${ apartment.main_pic }" alt="apartment pic"></a>
									<div class="card-body single-apartment-card">
										<h5 class="card-title"><a href="/${apartment.id}">${ apartment.address }</a></h5>
										<h6 class="card-subtitle">${ apartment.zip_code.id || apartment.zip_code[1]} ${ apartment.zip_code.town || apartment.zip_code[0]}</h6>
										<h6>${ Number(apartment.price).dotSeperator() } ISK</h6>
										<div class="d-flex justify-content-between">
											<div>
												<p>${ apartment.size } sqm</p>
											</div>
											<div>
												<p>Rooms: ${ apartment.rooms }</p>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					`
				})
				$('.apartments-list').html(newHTML.join(''))
				$('#apartmentsFound').text('Apartments found: ' + newHTML.length)
				if (newHTML.length === 0) {
					$('.apartments-list').html('<h2 style="text-align:center;width: 100%;">No apartments found with those search queries</h2>')
				}
				$("#order_by").val('a-z')
			},
			error: function(xhr, status, error) {
				console.error(xhr, status, error)
			}
		})
	})


	$('#submitFormHomeButton').on('click', (e) => {
		e.preventDefault()
		var searchText = $('#search_address').val()
		var minPrice = $("#min_price").val().numberize()
		var maxPrice = $("#max_price").val().numberize()
		var minSize = $('#min_size').val()
		var maxSize = $('#max_size').val()
		var rooms = $('#search_rooms').val()
		if(rooms == '6+') {
			rooms = '6'
		}
		var checked = $('.zip_option input:checked')
		zipcodes = $.map(checked, (input) => {
			return input.value
		})
		window.location.href = '/apartments?from_home=True&search_filter=' + searchText + '&min_price=' + minPrice + '&max_price=' + maxPrice + '&min_size=' + minSize + '&max_size=' + maxSize + '&rooms=' + rooms + '&zipcodes=' + zipcodes.join(',')

	})

	$('#order_by').on('change', function() {
  		let selected = this.value
		let apartments = $('.single-apartment')
		if (apartments.length === 0) return;
		switch(selected) {
			case 'a-z':
				apartments = apartments.sort(function(a, b) {
					if(a.getAttribute('data-address') < b.getAttribute('data-address')) { return -1; }
			 		if(a.getAttribute('data-address') > b.getAttribute('data-address')) { return 1; }
			 		return 0;
				})
				$('.apartments-list').html(apartments)
			break;
			case 'z-a':
				apartments = apartments.sort(function(a, b) {
					if(b.getAttribute('data-address') < a.getAttribute('data-address')) { return -1; }
			 		if(b.getAttribute('data-address') > a.getAttribute('data-address')) { return 1; }
			 		return 0;
				})
				$('.apartments-list').html(apartments)
			break;
			case 'price_lowest':
				apartments = apartments.sort(function(a, b) {
					return parseFloat(a.getAttribute('data-price')) - parseFloat(b.getAttribute('data-price'))
				})
				$('.apartments-list').html(apartments)
			break;
			case 'price_highest':
				apartments = apartments.sort(function(a, b) {
					return parseFloat(b.getAttribute('data-price')) - parseFloat(a.getAttribute('data-price'))
				})
				$('.apartments-list').html(apartments)
			break;
		}
	});

	$(function () {
		if(window.location.pathname === '/apartments/') {
			let min_price_django = $('#min_price_django')
			let max_price_django = $('#max_price_django')
			let min_size_django = $('#min_size_django')
			let max_size_django = $('#max_size_django')
			$('#min_price').val(Number(min_price_django.val().numberize()).dotSeperator())
			$('#max_price').val(Number(max_price_django.val().numberize()).dotSeperator())
			$('#min_size').val(Number(min_size_django.val().numberize()).dotSeperator())
			$('#max_size').val(Number(max_size_django.val().numberize()).dotSeperator())
			$("#slider-range").slider({
				values: [min_price_django.val().numberize(), max_price_django.val().numberize()]
			});
			$("#size-range").slider({
				values: [min_size_django.val().numberize(), max_size_django.val().numberize()]
			});
			$('#search_rooms').val($('#rooms_django').val())
			let zipcodes = $('#zipcodes_django').val()
			zipcodes = zipcodes.split(',')
			var options = $('.zip_option input')
			$.each(options, (key, input) => {
				if (zipcodes.indexOf(input.value) > -1) {
					input.checked = true
				}
			})
			if (zipcodes.length > 0 && zipcodes[0] !== "") {
				$('#howManyZips').text(zipcodes.length + ' zip code/s')
			}
		}
	})
	$('.featured_apartments').slick({
		slidesToShow: 1,
		fade: true,
		autoplay: true,
		arrows: false,
		autoplaySpeed: 5000,
		pauseOnHover: true
	});

	$('.newest_apartments').slick({
		infinite: true,
		speed: 300,
		slidesToShow: 4,
		slidesToScroll: 4,
		arrows: true,
		prevArrow: $('.prev_arrow'),
		nextArrow: $('.next_arrow'),
		responsive: [
			{
				breakpoint: 1024,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 3,
					infinite: true,
				}
			},
			{
				breakpoint: 600,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2
				}
			},
			{
				breakpoint: 480,
				settings: {
					slidesToShow: 1,
					slidesToScroll: 1
				}
			}
		]
	});

	$('.apartment_info_main_pic').slick({
		slidesToShow: 1,
		slidesToScroll: 1,
		fade: true,
		// asNavFor: $('.apartment_info_small')
	});
	$('.apartment_info_small').slick({
		rows: 4,
		slidesPerRow: 2,
		slidesToScroll: 1,
		// vertical: true,
		infinite: true,
		asNavFor: $('.apartment_info_main_pic'),
		focusOnSelect: true
	});


	$('#uploadImage').on('show.bs.modal', function (event) {
	  var button = $(event.relatedTarget)
	  var currentImg = button.data('current_img')

	  var modal = $(this)
	  modal.find('.modal-body input').val(currentImg)
	})
});
