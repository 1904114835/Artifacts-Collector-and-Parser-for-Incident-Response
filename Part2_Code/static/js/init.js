/*
 * Copyright (c) 2022 Frenify
 * Author: Frenify
 * This file is made for CURRENT TEMPLATE
*/


var AnorBody		= jQuery('body');
var AnorIsSafari 	= (/^((?!chrome|android).)*safari/i.test(navigator.userAgent));
if(AnorIsSafari){AnorBody.addClass('anor-safari');}
(function($){
  "use strict";
  
  
	var FrenifyAnor = {

		init: function(){
			FrenifyAnor.cursor();
			FrenifyAnor.countdown();
			FrenifyAnor.like();
			FrenifyAnor.follow();
			FrenifyAnor.share();
			FrenifyAnor.report();
			FrenifyAnor.follower();
			FrenifyAnor.BgImg();
			FrenifyAnor.imgToSVG();
			FrenifyAnor.totop();
			FrenifyAnor.select2();
			FrenifyAnor.counter();
			FrenifyAnor.tippy();
			FrenifyAnor.copyToClipboard();
			FrenifyAnor.searchFilterOpener();
			FrenifyAnor.hashtag();
			FrenifyAnor.filterItems();
			FrenifyAnor.closeFilter();
			FrenifyAnor.hideText();
			FrenifyAnor.graph();
			FrenifyAnor.accordion();
			FrenifyAnor.product__activity_filter();
			FrenifyAnor.product__action();
			FrenifyAnor.triggerMenu();
			FrenifyAnor.megamenu();
			FrenifyAnor.contactForm();
			FrenifyAnor.selectFromPopup();
			FrenifyAnor.flickitySlider();
			FrenifyAnor.actionButton();
			FrenifyAnor.introTab();
		},
		
		introTab: function(){
			$('.anor_fn_intro_tab .tab_switcher a').off().on('click',function(){
				var element = $(this);
				var parent	= element.closest('.anor_fn_intro_tab');
				var li		= element.parent();
				if(!li.hasClass('active')){
					li.addClass('active');
					li.siblings().removeClass('active');
					parent.find('.tab_item.active').removeClass('active');
					parent.find(element.attr('href')).addClass('active');
					// also enable/disable light/dark mode
					$('html').attr('data-skin',element.attr('class'));
				}
				return false;
			});
		},
		
		
		preloader: function(){
			var isMobile 	= /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ? true : false;
			var preloader 	= $('#preloader');
			if(preloader.length){
				setTimeout(function(){
					if (!isMobile) {
						setTimeout(function() {
							preloader.addClass('preloaded');
						}, 800);
						setTimeout(function() {
							preloader.remove();
						}, 2300);

					} else {
						preloader.remove();
					}
				}, 500);
			}	
		},
		
		sliderWidth: function(){
			var WW = $(window).width();
			$('.flickity_slider').each(function(){
				var element = $(this),
					width	= element.width(),
					item	= element.find('.carousel-cell'),
					cols	= element.data('cols'),
					gap		= element.data('gap'),
					cw;
				
				if(WW <= 1400 && WW > 1200){
					if(cols > 4){cols = 4;}
				}else if(WW < 1200 && WW > 1040){
					if(cols > 3){cols = 3;}
				}else if(WW < 1040 && WW > 768){
					if(cols > 2){cols = 2;}
				}else if(WW <= 768){
					if(cols > 1){cols = 1;}
				}
				
				if(!gap){gap = 40;}
				
				// in pixels
				cw = ((width - (cols - 1) * gap) / cols) + 'px';
				// in percentage (use this if there have unexpected width changes)
//				cw = (((width - (cols - 1) * gap) / cols) * 100) / width +'%';
				
				if(cols <= 1){cw = '100%';}
				item.css({width: cw,marginRight: gap + 'px'});
			});
		},
		
		safariFlickity: function(){
			$('.flickity_slider').each(function(){
				var element = $(this),
					item	= element.find('.carousel-cell'),
					gap		= element.data('gap');
				if(!gap){gap = 40;}
				element.css({marginLeft: '-' + gap + 'px'});
				item.css({paddingLeft: gap + 'px',marginBottom: gap + 'px'});
			});	
		},
		
		flickitySlider: function(){
			if(!AnorIsSafari){
				FrenifyAnor.sliderWidth();
			}else{
				FrenifyAnor.safariFlickity();
			}
			
			var inner = $(".cursor-inner"),
				outer = $(".cursor-outer");
			$('.flickity_slider').each(function(){
				var e = $(this),
					parent		= e.closest('.flickity_slider_wrap'),
					scrollBar 	= parent.find('.scrollBar .move');
				if(e.hasClass('ready')){return false;}
				e.addClass('ready');
				
				if (!AnorIsSafari){
					e.flickity({
						cellAlign: 'left',
						contain: true,
						prevNextButtons: false,
						pageDots: false,
						resize: true,
						groupCells: 1,
						selectedAttraction: 0.01,
						friction: 0.15,
						imagesLoaded: true
					});
					e.on( 'dragMove.flickity', function( event, pointer, moveVector  ) {
						inner.css({left: moveVector.x + 'px',top: moveVector.y + 'px'});
						outer.css({left: moveVector.x + 'px',top: moveVector.y + 'px'});
					});
					e.on( 'dragEnd.flickity', function() {
						inner.css({left: '0px',top:'0px'});
						outer.css({left: '0px',top:'0px'});
					});
					e.on( 'scroll.flickity', function( event, progress ) {
						progress = Math.max( 0, Math.min( 1, progress ) );
						if(scrollBar.data('type') === 'fill'){
							scrollBar.css({width: progress * 100+'%'});
						}else{
							scrollBar.css({left: progress * 75+'%'});
						}
					});
				}
					
			});
			
			
		},
		
		selectFromPopup: function(){
			$('.input_dd_list a').off().on('click',function(){
				var e = $(this),
					p = e.closest('.dd_filter');
				p.find('.input_wrapper input').val(e.text());
				
				// you can uncomment below code to stop closing function on click element
				p.removeClass('opened');
				
				return false;
			});
		},
		
		contactForm: function(){
			$(".contact_form #send_message").on('click', function(){
				var name 		= $(".contact_form #name").val();
				var email 		= $(".contact_form #email").val();
				var subject 	= $(".contact_form #subject").val();
				var message 	= $(".contact_form #message").val();
				var success     = $(".contact_form .returnmessage").data('success');

				$(".contact_form .returnmessage").empty(); //To empty previous error/success message.
				//checking for blank fields	
				if(name===''||email===''||message===''){
					$('.contact_form div.empty_notice').slideDown(500).delay(2000).slideUp(500);
				}
				else{
					// Returns successful data submission message when the entered information is stored in database.
					$.post("modal/contact.php",{ ajax_name: name, ajax_email: email, ajax_subject: subject, ajax_message:message}, function(data) {

						$(".contact_form .returnmessage").append(data);//Append returned message to message paragraph


						if($(".contact_form .returnmessage span.contact_error").length){
							$(".contact_form .returnmessage").slideDown(500).delay(2000).slideUp(500);		
						}else{
							$(".contact_form .returnmessage").append("<span class='contact_success'>"+ success +"</span>");
							$(".contact_form .returnmessage").slideDown(500).delay(4000).slideUp(500);
						}

						if(data===""){
							$("#contact_form")[0].reset();//To reset form fields on success
						}

					});
				}
				return false; 
			});
		},
		
		megamenu: function(){
			$('.anor_fn_header .main_menu > li').each(function() {
				var item 		= $(this),
					megaDiv		= item.find(".anor_fn_megamenu");
				

				// Mega Menu Position Fixes
				if(megaDiv.length){
					var parentOffset	= item.parent().offset().left,
						parentPosition	= item.parent().position().left,
						mainOffset		= parentOffset - parentPosition;
					megaDiv.css({left: (item.offset().left * -1), paddingLeft:mainOffset, paddingRight:mainOffset});
				}	
			});


			var navW 		= 	$('.anor_fn_main').width();
			var megaMenu 	= 	$('.anor_fn_megamenu');

			megaMenu.css({width:navW});
		},
		
		
		
		triggerMenu: function(){
			var hamburger 		= $('.hamburger');
			var mobileMenu		= $('.anor_fn_mobile_menu .dropdown');
			var mobileMenuList	= mobileMenu.find('a');

			hamburger.on('click',function(){
				var element 	= $(this);

				if(element.hasClass('is-active')){
					element.removeClass('is-active');
					mobileMenu.slideUp();
				}else{
					element.addClass('is-active');
					mobileMenu.slideDown();
				}
				return false;
			});

			mobileMenuList.on('click',function(){
				$('.hamburger').removeClass('is-active');
				mobileMenu.slideUp();
				return false;
			});
			
			
			var nav = $('.vert_menu');
			nav.find('a').off().on('click', function(e){
				var element 			= $(this);
				var parentItem			= element.parent('li');
				var parentItems			= element.parents('li');
				var parentUls			= parentItem.parents('ul.sub-menu');
				var subMenu				= element.next();
				var allSubMenusParents 	= nav.find('li');

				allSubMenusParents.removeClass('opened');

				if(subMenu.length){
					e.preventDefault();

					if(!(subMenu.parent('li').hasClass('active'))){
						if(!(parentItems.hasClass('opened'))){parentItems.addClass('opened');}

						allSubMenusParents.each(function(){
							var el = $(this);
							if(!el.hasClass('opened')){el.find('ul.sub-menu').slideUp();}
						});

						allSubMenusParents.removeClass('active');
						parentUls.parent('li').addClass('active');
						subMenu.parent('li').addClass('active');
						subMenu.slideDown();


					}else{
						subMenu.parent('li').removeClass('active');
						subMenu.slideUp();
					}
					return false;
				}
			});
		},
		
		product__action: function(){
			$('.product_action .action_btn').off().on('click',function(){
				$(this).closest('.product_action').toggleClass('opened');
				return false;
			});
			$('.product_action .action_popup').on('click',function(e){
				e.stopPropagation();
			});
			$(window).on('click',function(){
				$('.product_action').removeClass('opened');
			});
		},
		
		countdown: function(){
			$('.fn__countdown').each(function(){
				var e 		= $(this),
					t 		= e.data('type'),
					dd 		= e.data('due-date');
				if(!e.hasClass('ready')){
					e.addClass('ready');
					if(t === 'date'){
						var countDownDate = new Date(dd).getTime();

						// Update the count down every 1 second
						var x = setInterval(function() {

							// Get today's date and time
							var now = new Date().getTime();

							// Find the distance between now and the count down date
							var distance = countDownDate - now;

							// Time calculations for days, hours, minutes and seconds
							var days = Math.floor(distance / (1000 * 60 * 60 * 24));
							var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
							var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
							var seconds = Math.floor((distance % (1000 * 60)) / 1000);

							days 	= days < 9 ? '0' + days : days;
							hours 	= hours < 9 ? '0' + hours : hours;
							minutes = minutes < 9 ? '0' + minutes : minutes;
							seconds = seconds < 9 ? '0' + seconds : seconds;

							// Display the result
							e.html(days + "d " + hours + "h " + minutes + "m " + seconds + "s");

							// If the count down is finished, write some text
							if (distance < 0) {
								clearInterval(x);
							}
						}, 1000);
					}else if(t === 'ever'){
						var ever 			= parseInt(e.data('days'))* 86400 + parseInt(e.data('hours'))* 3600 + parseInt(e.data('minutes')) * 60 + parseInt(e.data('seconds'));
						var y 				= setInterval(function(){
							var days 		= Math.floor(ever / 86400);
							var hours 		= Math.floor((ever % 86400) / 3600);
							var minutes 	= Math.floor((ever % 3600) / 60);
							var seconds 	= Math.floor((ever % 60));
							
							
							
							days			= (days < 10) ? '0' + days : days;
							hours			= (hours < 10) ? '0' + hours : hours;
							minutes 		= (minutes < 10) ? '0' + minutes : minutes;
							seconds 		= (seconds < 10) ? '0' + seconds : seconds;
							
							e.html(days + "d " + hours + "h " + minutes + "m " + seconds + "s");
							ever			= ever - 1;
							if(ever < 0){
								clearInterval(y);
							}
						}, 1000);
					}
				}
			});
		},
		
		product_activity_filter_remove: function(){
			$('.anor_fn_product_activity .selected_filter a').off().on('click',function(){
				var e = $(this),
					p	= e.closest('.anor_fn_product_activity'),
					s	= e.closest('.selected_filter'),
					id 	= s.data('id');
				s.remove();
				p.find('.filter_list a[data-id="'+id+'"]').removeClass('selected');
				if(p.find('.filter_list .selected').length === 0){
					p.find('.pa_item').addClass('active');
				}else{
					p.find('.pa_item[data-id="'+id+'"]').removeClass('active');
				}
				return false;
			});
		},
		
		product__activity_filter: function(){
			// filter opener and closer
			$('.anor_fn_product_activity .filter_opener').off().on('click',function(){
				$(this).closest('.filter').toggleClass('opened');
				return false;
			});
			$('.anor_fn_product_activity .filter_list').on('click',function(e){
				e.stopPropagation();
			});
			$(window).on('click',function(){
				$('.anor_fn_product_activity .filter').removeClass('opened');
			});
			
			
			// filter button
			$('.anor_fn_product_activity .filter_list a').off().on('click',function(){
				var e 	= $(this),
					p	= e.closest('.anor_fn_product_activity'),
					id 	= e.data('id');
				if(!e.hasClass('selected')){
					if(p.find('.filter_list .selected').length === 0){
						p.find('.pa_item').removeClass('active');
					}
					e.addClass('selected');
					p.find('.pa_item[data-id="'+id+'"]').addClass('active');
					p.find('.filters').append('<div class="selected_filter" data-id="'+id+'"><a href="#">'+e.text()+'<img src="svg/cancel.svg" alt="" class="fn__svg"></a></div>');
					FrenifyAnor.imgToSVG();
					FrenifyAnor.product_activity_filter_remove();
				}else{
					e.removeClass('selected');
					p.find('.selected_filter[data-id="'+id+'"]').remove();
					if(p.find('.filter_list .selected').length === 0){
						p.find('.pa_item').addClass('active');
					}else{
						p.find('.pa_item[data-id="'+id+'"]').removeClass('active');
					}
				}
				return false;
			});
			FrenifyAnor.product_activity_filter_remove();
			
		},
		
		accordion: function(){
			$('.anor_fn_accordion .accordion_header a').off().on('click',function(){
				$(this).closest('.anor_fn_accordion').toggleClass('closed');
				return false;
			});
		},
		
		monthNames: function(i){
			var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
			return monthNames[i];
		},
		
		graph: function(){
			if(!$('#myChart').length){
				return false;
			}
			var y = ['2022/03/27','2022/03/28','2022/03/29','2022/03/30','2022/03/31','2022/04/01','2022/04/02'];
			var x = [1.15, 1.57, 1.23, 2.18, 2.3, 1.55, 2.41];
			var sales = [15, 20, 37, 43, 30, 53, 24];
			var graphBgColor = '#31b13a';
			var graphBorderColor = '#31b13a';
			var priceText = 'Avg. Price';
			var volumeText = 'Volume';
			var numSaleText = 'Num. Sales';
			
			
			// modified y 
			var yRE = y.map((element, index) => {
				var dateObj = new Date(element);
				var month 	= dateObj.getMonth()+1; //months from 1-12
				var day 	= dateObj.getDate();
				return 	('0' + month).slice(-2) + '/' + ('0' + day).slice(-2);
			});
			
			var data = {
				labels: y,
				datasets: [{
					backgroundColor: graphBgColor,
					borderColor: graphBorderColor,
					tension: 0.4,
					data: x
				}]
			};

			var config = {
				type: 'line',
				data: data,
				options: {
					maintainAspectRatio: false,
					scales: {
						y: {
							suggestedMin: 0,
//							suggestedMax: 3,
							ticks: {
								stepSize: 1
							}
						}
					},
					interaction: {
						intersect: false,
						mode: 'index',
					},
					plugins: {
						legend: {
							display: false
						},
						tooltip: {
							enabled: false,
							external: function(context) {
								// Tooltip Element
								var tooltipEl 			= document.getElementById('chartjs-tooltip');
								// Create element on first render
								if (!tooltipEl) {
									tooltipEl 			= document.createElement('div');
									tooltipEl.id 		= 'chartjs-tooltip';
									document.body.appendChild(tooltipEl);
								}

								// Hide if no tooltip
								var tooltipModel = context.tooltip;
								if (tooltipModel.opacity === 0) {
									tooltipEl.style.opacity = 0;
									return;
								}

								// Set caret Position
								tooltipEl.classList.remove('above', 'below', 'no-transform');
								if (tooltipModel.yAlign) {
									tooltipEl.classList.add(tooltipModel.yAlign);
								} else {
									tooltipEl.classList.add('no-transform');
								}

								function getBody(bodyItem) {
									return bodyItem.lines;
								}

								// Set Text
								if (tooltipModel.body) {
									var titleLines = tooltipModel.title || [];
									var bodyLines = tooltipModel.body.map(getBody);

									var innerHtml = '';

									titleLines.forEach(function(title) {
										var dateObj = new Date(title);
										var month 	= dateObj.getMonth(); //months from 1-12
										var day 	= dateObj.getDate();
										var year 	= dateObj.getFullYear();
										title 		= FrenifyAnor.monthNames(month) + ' ' + day + ', ' + year;
										innerHtml += '<h3 class="fn_title">' + title + '</h3>';
									});

									bodyLines.forEach(function(body) {
										innerHtml += '<p>' + priceText + ': ' + body + '</p>';
//										innerHtml += '<p>' + volumeText + ': ' + parseFloat(body) * sales[0] + '</p>';
									});

									tooltipEl.innerHTML = innerHtml;
								}

								var position = context.chart.canvas.getBoundingClientRect();
								var bodyFont = Chart.helpers.toFont(tooltipModel.options.bodyFont);

								// Display, position, and set styles for font
								tooltipEl.style.opacity = 1;
								tooltipEl.style.position = 'absolute';
								tooltipEl.style.left = position.left + window.pageXOffset + tooltipModel.caretX + 'px';
								tooltipEl.style.top = position.top + window.pageYOffset + tooltipModel.caretY + 'px';
								tooltipEl.style.font = bodyFont.string;
								tooltipEl.style.padding = tooltipModel.padding + 'px ' + tooltipModel.padding + 'px';
								tooltipEl.style.pointerEvents = 'none';
							}

						}
					}
				}
			};
			var myChart = new Chart(
				document.getElementById('myChart'),
				config
			);
		},
		
		hideText: function(){
			$('.anor_fn_hide_text').each(function(){
				var e = $(this);
				if(e.height() > e.data('max')*e.data('height')){
					e.addClass('ready');
				}else{
					e.removeClass('ready').addClass('enough');
				}
			});
			$('.anor_fn_hide_text .read_more').on('click',function(){
				var e = $(this);
				var p = e.closest('.anor_fn_hide_text');
				if(p.hasClass('ready')){
					p.removeClass('ready');
					e.text(e.data('less'));
				}else{
					p.addClass('ready');
					e.text(e.data('more'));
				}
				return false;
			});
			
			// Show More Button in single product.html page
			$('.hide_text .show_more').on('click',function(){
				var e = $(this);
				var p = e.closest('.hide_text');
				if(!p.hasClass('ready')){
					p.addClass('ready');
					e.text(e.data('less'));
				}else{
					p.removeClass('ready');
					e.text(e.data('more'));
				}
				return false;
			});
		},
		
		closeFilter: function(){
			if($(window).width() < 1041){
				$('.anor_fn_tabs').addClass('closed');
			}	
		},
		
		filterItems: function(){
			$('.filter_item .filter_item__header a').off().on('click',function(){
				$(this).closest('.filter_item').toggleClass('closed');
				return false;
			});
			$('.anor_fn_filters .filter_header a').off().on('click',function(){
				$(this).closest('.anor_fn_tabs').toggleClass('closed');
				setTimeout(function(){
					FrenifyAnor.hashtag();
				},400);
				return false;
			});
		},
		
		hashtag: function(){
			var ccc 			= $('.anor_fn_tabs .tab_filter .ccc');
			var element 		= $('.anor_fn_tabs .tab_filter .current a');
			$('.anor_fn_tabs .tab_filter a').on('mouseenter',function(){
				var e 			= $(this);
				FrenifyAnor.currentLink(ccc,e);
			});
			$('.anor_fn_tabs .tab_filter').on('mouseleave',function(){
				element 		= $('.anor_fn_tabs .tab_filter .current a');
				FrenifyAnor.currentLink(ccc,element);
			});
			FrenifyAnor.currentLink(ccc,element);
		},
		
		currentLink: function(ccc,e){
			if(!e.length){return false;}
			var left 		= e.offset().left;
			var top 		= e.offset().top;
			var width		= e.outerWidth();
			var filter		= $('.anor_fn_tabs .tab_filter');
			var menuleft 	= filter.offset().left;
			var menuTop 	= filter.offset().top;
			if(e.parent().hasClass('button')){
				width = 0;
			}
			ccc.css({left: (left-menuleft) + 'px',width: width + 'px',top: (top-menuTop+e.outerHeight()-2) + 'px',bottom: 'auto'});
		},
		
		searchFilterOpener: function(){
			$('.input_wrapper').off().on('click',function(e){
				e.stopPropagation();
				var parent = $(this).closest('.dd_filter');
				if(parent.hasClass('opened')){
					$('.dd_filter').removeClass('opened');
				}else{
					$('.dd_filter').removeClass('opened');
					parent.addClass('opened');
				}
			});
			$('.input_dd_list').on('click',function(e){
				e.stopPropagation();
			});
			$(window).on('click',function(){
				$('.dd_filter').removeClass('opened');
			});
		},
		
		clipboard: function(element){
			var $temp = $("<input>");
			$("body").append($temp);
			$temp.val($(element).text()).select();
			document.execCommand("copy");
			$temp.remove();
		},
		
		copyToClipboard: function(){
			$('.fn__id').on('click',function(){
				var element = $(this);
				FrenifyAnor.clipboard(element);
				element.attr('data-tippy-content', element.data('copied'));
				var instance = tippy(element[0]);
				instance.show();
				setTimeout(function(){
					instance.hide();
					instance.disable();
				},500);
				return false;
			});
		},
		
		tippy: function(){
			tippy('.tippy', {
			  	arrow: true,
			  	animation: 'shift-toward',
			});
			tippy('.tippy_right', {
			  	arrow: true,
			  	animation: 'shift-toward',
				placement: 'right',
			});	
			tippy('.tippy_left', {
			  	arrow: true,
			  	animation: 'shift-toward',
				placement: 'left',
			});	
			tippy('.tippy_bottom', {
			  	arrow: true,
			  	animation: 'shift-toward',
				placement: 'bottom',
			});	
		},
		
		counter: function(){
			var element = $('.anor_fn_counter');
			element.each(function() {
				var el 	= $(this);
				var decimal	= parseInt(el.data('decimal'));
				el.waypoint({
					handler: function(){
						if(!el.hasClass('stop')){
							el.addClass('stop').countTo({
								refreshInterval: 50,
								decimals: decimal,
								formatter: function (value, options) {
									return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
								},	
							});
						}
					},
					offset:'90%'	
				});
			});
		},
		
		select2: function(){
			$('.anor_fn_modal select').select2();	
		},
		
		totop: function (){
			$(".anor_fn_footer .totop").off().on('click', function(e) {
				e.preventDefault();    
				$("html, body").animate({ scrollTop: 0 }, 1200);
				return false;
			});
		},
		
		cursor: function () {
			var myCursor = $('.frenify-cursor');
			if (myCursor.length) {
				if (AnorBody.length) {
					const e = document.querySelector(".cursor-inner"),
						t 	= document.querySelector(".cursor-outer");
					var n, i = 0,
						o = !1;
					var buttons = ".anor_fn_upload_media label, .checkbox, .input_wrapper, .anor_fn_modal .modal_closer, a, input[type='submit'], .cursor-link, button";
					var sliders = ".flickity-viewport, .owl-carousel, .cursor-link";
					// link mouse enter + move
					window.onmousemove = function(s) {
						o || (t.style.transform = "translate(" + s.clientX + "px, " + s.clientY + "px)"), e.style.transform = "translate(" + s.clientX + "px, " + s.clientY + "px)", n = s.clientY, i = s.clientX
					}, AnorBody.on("mouseenter", buttons, function() {
						e.classList.add("cursor-hover"), t.classList.add("cursor-hover")
					}), AnorBody.on("mouseleave", buttons, function() {
						$(this).is("a") && $(this).closest(".cursor-link").length || (e.classList.remove("cursor-hover"), t.classList.remove("cursor-hover"))
					}), e.style.visibility = "visible", t.style.visibility = "visible";
					
					
					// slider mouse enter
					AnorBody.on('mouseenter', sliders, function(){
						e.classList.add('cursor-slider');
						t.classList.add('cursor-slider');
					}).on('mouseleave', sliders,function(){
						e.classList.remove('cursor-slider');
						t.classList.remove('cursor-slider');
					});
					
					// slider mouse hold
					AnorBody.on('mousedown', sliders, function(){
						e.classList.add('mouse-down');
						t.classList.add('mouse-down');
					}).on('mouseup', sliders, function(){
						e.classList.remove('mouse-down');
						t.classList.remove('mouse-down');
					});
				}
			}
		},
		
		share: function(){
			var btn 		= $('a.anor_fn_share_item');
			var modal_box	= $('.anor_fn_modal.share_box');
			btn.off().on('click',function(){
				var button 	= $(this),
					title	= button.data('title');
				
				// change its title
				modal_box.find('.share_title').html(title);
				
				
				// you can change social icons URL based on item URL and image
				var URL				= 'URL';		// just get a URL of shared item here and share box will automatically generate share URL for all gaven social platforms
				var mediaSRC		= 'mediaSRC';	// just get a media URL of shared item here and share box will automatically generate share URL for all gaven social platforms
				// ..............................
				// ..............................
				var facebookURL 	= 'https://www.facebook.com/sharer/sharer.php?u='+URL+'" target="_blank"';
				var twitterURL		= 'https://twitter.com/share?url='+URL+'" target="_blank"';
				var pinterestURL	= 'http://pinterest.com/pin/create/button/?url='+URL+'&amp;media='+mediaSRC+'" target="_blank"';
				var linkedinURL		= 'http://linkedin.com/shareArticle?mini=true&amp;url='+URL+'&amp;" target="_blank"';
				var emailURL		= 'mailto:?amp;body='+URL+'" target="_blank"';
				var vkURL			= 'https://www.vk.com/share.php?url='+URL+'" target="_blank"';
				modal_box.find('.facebook').attr('href',facebookURL);
				modal_box.find('.twitter').attr('href',twitterURL);
				modal_box.find('.pinterest').attr('href',pinterestURL);
				modal_box.find('.linkedin').attr('href',linkedinURL);
				modal_box.find('.email').attr('href',emailURL);
				modal_box.find('.vk').attr('href',vkURL);
				// ..............................
				// ..............................
				
				
				// open share box
				modal_box.addClass('opened');
				return false;
			});
			modal_box.find('.modal_closer').off().on('click',function(){
				modal_box.removeClass('opened');
				return false;
			});
		},
		
		follower: function(){
			var btn 		= $('a.anor_fn_follower');
			var modal_box	= $('.anor_fn_modal.follower_box');
			btn.off().on('click',function(){
				var button 		= $(this),
					authorID	= button.data('id'),
					action		= button.data('action');
				
				
				if(!button.hasClass('loading')){
					// change its title
					modal_box.find('.modal_title').html(button.text());
					
					// do your ajax here with author ID and action
					// ..............................
					// ..............................
					// ajax ends
					button.removeClass('loading');
					// -----------------
				}
				
				
				
				
				// open modal box
				modal_box.addClass('opened');
				return false;
			});
			modal_box.find('.modal_closer').off().on('click',function(){
				modal_box.removeClass('opened');
				return false;
			});
		},
		
		report: function(){
			var btn 		= $('a.anor_fn_report_item');
			var modal_box	= $('.anor_fn_modal.report_box');
			btn.off().on('click',function(){
				var button 	= $(this),
					title	= button.data('title');
				
				// change its title
				modal_box.find('.fn_title').html(title);
				
				
				
				
				// open modal box
				modal_box.addClass('opened');
				return false;
			});
			modal_box.find('.modal_closer').off().on('click',function(){
				modal_box.removeClass('opened');
				return false;
			});
		},
		
		
		actionButton: function(){
			$('.action_collection .action_btn').off().on('click',function(){
				var parent = $(this).closest('.action_collection');
				if(parent.hasClass('opened')){
					$('.action_collection').removeClass('opened');
				}else{
					$('.action_collection').removeClass('opened');
					parent.addClass('opened');
				}
				return false;
			});
			$('.action_box .action_btn').off().on('click',function(){
				var parent = $(this).closest('.action_box');
				if(parent.hasClass('opened')){
					$('.action_box').removeClass('opened');
				}else{
					$('.action_box').removeClass('opened');
					parent.addClass('opened');
				}
				return false;
			});
			$('.author_action .action_btn').off().on('click',function(){
				var parent = $(this).closest('.author_action');
				if(parent.hasClass('opened')){
					$('.author_action').removeClass('opened');
				}else{
					$('.author_action').removeClass('opened');
					parent.addClass('opened');
				}
				return false;
			});
			$('.action_popup,.anor_fn_modal').on('click',function(e){
				e.stopPropagation();
			});
			$(window).on('click',function(){
				$('.author_action').removeClass('opened');
				$('.action_box').removeClass('opened');
			});
		},
		
		like: function(){
			$('a.anor_fn_like').off().on('click',function(){
				var button 		= $(this),
					itemID		= button.data('id'),
					itemTitle	= button.data('title'); 
				
				// if button has not been clicked && not going a process of loading (ajax function) in order to avoid previous clicking on button button
				if(!button.hasClass('liked') && !button.hasClass('loading')){
					
					// do your ajax here with button ID and title
					// ..............................
					// ..............................
					// ajax ends
					button.removeClass('loading');
					// -----------------
					
					
					// now your button has been liked
					button.addClass('liked');
				}
				return false;
			});
			
			
			$('a.anor_fn_like_full').off().on('click',function(){
				var button 		= $(this),
					itemID		= button.data('id'),
					itemTitle	= button.data('title'); 
				
				// if button has not been clicked && not going a process of loading (ajax function) in order to avoid previous clicking on button button
				if(!button.hasClass('liked') && !button.hasClass('loading')){
					
					// do your ajax here with button ID and title
					// ..............................
					// ..............................
					// ajax ends
					button.removeClass('loading');
					// -----------------
					
					// change like count number
					// you have to get count from ajax and change count's value with yours one
					var count 	= parseInt(button.find('.count').text());
					button.find('.count').text(count+1);
					
					
					// now your button has been liked
					button.addClass('liked');
				}
				return false;
			});
		},
		
		follow: function(){
			$('a.anor_fn_follow').off().on('click',function(){
				var button 		= $(this),
					itemID		= button.data('id'),
					followed	= button.data('followed'); 
				
				// if button has not been clicked && not going a process of loading (ajax function) in order to avoid previous clicking on the button
				if(!button.hasClass('followed') && !button.hasClass('loading')){
					
					// do your ajax here with item ID
					// ..............................
					// ..............................
					// ajax ends
					button.removeClass('loading');
					// -----------------
					
					
					// now your button has been followed
					button.find('.text').text(followed);
					button.addClass('followed');
				}
				return false;
			});
		},
		
		
		
		imgToSVG: function(){
			$('img.fn__svg').each(function(){
				var img 		= $(this);
				var imgClass	= img.attr('class');
				var imgURL		= img.attr('src');

				$.get(imgURL, function(data) {
					var svg 	= $(data).find('svg');
					if(typeof imgClass !== 'undefined') {
						svg 	= svg.attr('class', imgClass+' replaced-svg');
					}
					img.replaceWith(svg);

				}, 'xml');

			});	
		},

	  	BgImg: function(){
			var div = $('*[data-bg-img]');
			div.each(function(){
				var element = $(this);
				var attrBg	= element.attr('data-bg-img');
				var dataBg	= element.data('bg-img');
				if(typeof(attrBg) !== 'undefined'){
					element.css({backgroundImage:'url('+dataBg+')'});
				}
			});
		},
    
  	};
  	
	
	// READY Functions
	$(document).ready(function(){
		FrenifyAnor.init();
		setTimeout(function(){
			FrenifyAnor.hashtag();
			FrenifyAnor.megamenu();
		},150);
	});
	
	// RESIZE Functions
	$(window).on('resize',function(){
		FrenifyAnor.hashtag();
		FrenifyAnor.closeFilter();
		FrenifyAnor.megamenu();
		if(!AnorIsSafari){
			FrenifyAnor.sliderWidth();
		}
	});
	
	// LOAD Functions
	$(window).load('body', function(){
		FrenifyAnor.preloader();
	});
	$(window).on('load',function(){
		
		FrenifyAnor.megamenu();
		setTimeout(function(){
			
		},10);
	});
  	
})(jQuery);