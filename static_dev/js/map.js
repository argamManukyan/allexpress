/* Modal */
+function ($) {
  'use strict';
  var Modal = function (element, options) {
    this.options             = options
    this.$body               = $(document.body)
    this.$element            = $(element)
    this.$dialog             = this.$element.find('.modal-dialog')
    this.$backdrop           = null
    this.isShown             = null
    this.originalBodyPad     = null
    this.scrollbarWidth      = 0
    this.ignoreBackdropClick = false

    if (this.options.remote) {
      this.$element
        .find('.modal-content')
        .load(this.options.remote, $.proxy(function () {
          this.$element.trigger('loaded.bs.modal')
        }, this))
    }
  }

  Modal.VERSION  = '3.3.7'

  Modal.TRANSITION_DURATION = 300
  Modal.BACKDROP_TRANSITION_DURATION = 150

  Modal.DEFAULTS = {
    backdrop: true,
    keyboard: true,
    show: true
  }

  Modal.prototype.toggle = function (_relatedTarget) {
    return this.isShown ? this.hide() : this.show(_relatedTarget)
  }

  Modal.prototype.show = function (_relatedTarget) {
    var that = this
    var e    = $.Event('show.bs.modal', { relatedTarget: _relatedTarget })

    this.$element.trigger(e)

    if (this.isShown || e.isDefaultPrevented()) return

    this.isShown = true

    this.checkScrollbar()
    this.setScrollbar()
    this.$body.addClass('modal-open')

    this.escape()
    this.resize()

    this.$element.on('click.dismiss.bs.modal', '[data-dismiss="modal"]', $.proxy(this.hide, this))

    this.$dialog.on('mousedown.dismiss.bs.modal', function () {
      that.$element.one('mouseup.dismiss.bs.modal', function (e) {
        if ($(e.target).is(that.$element)) that.ignoreBackdropClick = true
      })
    })
    this.backdrop(function () {
      var transition = $.support.transition && that.$element.hasClass('fade')

      if (!that.$element.parent().length) {
        that.$element.appendTo(that.$body) // don't move modals dom position
      }

      that.$element
        .show()
        .scrollTop(0)

      that.adjustDialog()

      if (transition) {
        that.$element[0].offsetWidth // force reflow
      }

      that.$element.addClass('in')

      that.enforceFocus()

      var e = $.Event('shown.bs.modal', { relatedTarget: _relatedTarget })

      transition ?
        that.$dialog // wait for modal to slide in
          .one('bsTransitionEnd', function () {
            that.$element.trigger('focus').trigger(e)
          })
          .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
        that.$element.trigger('focus').trigger(e)
    })
  }
  Modal.prototype.hide = function (e) {
    if (e) e.preventDefault()

    e = $.Event('hide.bs.modal')

    this.$element.trigger(e)

    if (!this.isShown || e.isDefaultPrevented()) return

    this.isShown = false

    this.escape()
    this.resize()

    $(document).off('focusin.bs.modal')

    this.$element
      .removeClass('in')
      .off('click.dismiss.bs.modal')
      .off('mouseup.dismiss.bs.modal')

    this.$dialog.off('mousedown.dismiss.bs.modal')

    $.support.transition && this.$element.hasClass('fade') ?
      this.$element
        .one('bsTransitionEnd', $.proxy(this.hideModal, this))
        .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
      this.hideModal()
  }
  Modal.prototype.enforceFocus = function () {
    $(document)
      .off('focusin.bs.modal') // guard against infinite focus loop
      .on('focusin.bs.modal', $.proxy(function (e) {
        if (document !== e.target &&
            this.$element[0] !== e.target &&
            !this.$element.has(e.target).length) {
          this.$element.trigger('focus')
        }
      }, this))
  }
  Modal.prototype.escape = function () {
    if (this.isShown && this.options.keyboard) {
      this.$element.on('keydown.dismiss.bs.modal', $.proxy(function (e) {
        e.which == 27 && this.hide()
      }, this))
    } else if (!this.isShown) {
      this.$element.off('keydown.dismiss.bs.modal')
    }
  }
  Modal.prototype.resize = function () {
    if (this.isShown) {
      $(window).on('resize.bs.modal', $.proxy(this.handleUpdate, this))
    } else {
      $(window).off('resize.bs.modal')
    }
  }
  Modal.prototype.hideModal = function () {
    var that = this
    this.$element.hide()
    this.backdrop(function () {
      that.$body.removeClass('modal-open')
      that.resetAdjustments()
      that.resetScrollbar()
      that.$element.trigger('hidden.bs.modal')
    })
  }
  Modal.prototype.removeBackdrop = function () {
    this.$backdrop && this.$backdrop.remove()
    this.$backdrop = null
  }
  Modal.prototype.backdrop = function (callback) {
    var that = this
    var animate = this.$element.hasClass('fade') ? 'fade' : ''

    if (this.isShown && this.options.backdrop) {
      var doAnimate = $.support.transition && animate

      this.$backdrop = $(document.createElement('div'))
        .addClass('modal-backdrop ' + animate)
        .appendTo(this.$body)

      this.$element.on('click.dismiss.bs.modal', $.proxy(function (e) {
        if (this.ignoreBackdropClick) {
          this.ignoreBackdropClick = false
          return
        }
        if (e.target !== e.currentTarget) return
        this.options.backdrop == 'static'
          ? this.$element[0].focus()
          : this.hide()
      }, this))

      if (doAnimate) this.$backdrop[0].offsetWidth // force reflow

      this.$backdrop.addClass('in')

      if (!callback) return

      doAnimate ?
        this.$backdrop
          .one('bsTransitionEnd', callback)
          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
        callback()

    } else if (!this.isShown && this.$backdrop) {
      this.$backdrop.removeClass('in')

      var callbackRemove = function () {
        that.removeBackdrop()
        callback && callback()
      }
      $.support.transition && this.$element.hasClass('fade') ?
        this.$backdrop
          .one('bsTransitionEnd', callbackRemove)
          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
        callbackRemove()

    } else if (callback) {
      callback()
    }
  }

  // these following methods are used to handle overflowing modals
  Modal.prototype.handleUpdate = function () {
    this.adjustDialog()
  }
  Modal.prototype.adjustDialog = function () {
    var modalIsOverflowing = this.$element[0].scrollHeight > document.documentElement.clientHeight

    this.$element.css({
      paddingLeft:  !this.bodyIsOverflowing && modalIsOverflowing ? this.scrollbarWidth : '',
      paddingRight: this.bodyIsOverflowing && !modalIsOverflowing ? this.scrollbarWidth : ''
    })
  }
  Modal.prototype.resetAdjustments = function () {
    this.$element.css({
      paddingLeft: '',
      paddingRight: ''
    })
  }
  Modal.prototype.checkScrollbar = function () {
    var fullWindowWidth = window.innerWidth
    if (!fullWindowWidth) { // workaround for missing window.innerWidth in IE8
      var documentElementRect = document.documentElement.getBoundingClientRect()
      fullWindowWidth = documentElementRect.right - Math.abs(documentElementRect.left)
    }
    this.bodyIsOverflowing = document.body.clientWidth < fullWindowWidth
    this.scrollbarWidth = this.measureScrollbar()
  }
  Modal.prototype.setScrollbar = function () {
    var bodyPad = parseInt((this.$body.css('padding-right') || 0), 10)
    this.originalBodyPad = document.body.style.paddingRight || ''
    if (this.bodyIsOverflowing) this.$body.css('padding-right', bodyPad + this.scrollbarWidth)
  }
  Modal.prototype.resetScrollbar = function () {
    this.$body.css('padding-right', this.originalBodyPad)
  }
  Modal.prototype.measureScrollbar = function () { // thx walsh
    var scrollDiv = document.createElement('div')
    scrollDiv.className = 'modal-scrollbar-measure'
    this.$body.append(scrollDiv)
    var scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth
    this.$body[0].removeChild(scrollDiv)
    return scrollbarWidth
  }

  // MODAL PLUGIN DEFINITION
  function Plugin(option, _relatedTarget) {
    return this.each(function () {
      var $this   = $(this)
      var data    = $this.data('bs.modal')
      var options = $.extend({}, Modal.DEFAULTS, $this.data(), typeof option == 'object' && option)

      if (!data) $this.data('bs.modal', (data = new Modal(this, options)))
      if (typeof option == 'string') data[option](_relatedTarget)
      else if (options.show) data.show(_relatedTarget)
    })
  }

  var old = $.fn.modal
  $.fn.modal             = Plugin
  $.fn.modal.Constructor = Modal

  // MODAL NO CONFLICT
  $.fn.modal.noConflict = function () {
    $.fn.modal = old
    return this
  }

  // MODAL DATA-API
  $(document).on('click.bs.modal.data-api', '[data-toggle="modal"]', function (e) {
    var $this   = $(this)
    var href    = $this.attr('href')
    var $target = $($this.attr('data-target') || (href && href.replace(/.*(?=#[^\s]+$)/, ''))) // strip for ie7
    var option  = $target.data('bs.modal') ? 'toggle' : $.extend({ remote: !/#/.test(href) && href }, $target.data(), $this.data())

    if ($this.is('a')) e.preventDefault()

    $target.one('show.bs.modal', function (showEvent) {
      if (showEvent.isDefaultPrevented()) return // only register focus restorer if modal will actually get shown
      $target.one('hidden.bs.modal', function () {
        $this.is(':visible') && $this.trigger('focus')
      })
    })
    Plugin.call($target, option, this)
  })

}(jQuery);

/* Map*/
  ymaps.ready(init);
	    function init() {
		// Стоимость за километр.
		var DELIVERY_TARIFF = 100,
		    // Минимальная стоимость.
		    MINIMUM_COST = 300,
		    myMap = new ymaps.Map('map', {
			center: [60.906882, 30.067233],
			zoom: 5,
			controls: []
		    }),
		    // Создадим панель маршрутизации.
		    routePanelControl = new ymaps.control.RoutePanel({
			options: {
			    // Добавим заголовок панели.
			    showHeader: true,
			    title: 'Նշեք առաքման հասցեն'
			}
		    }),
		    zoomControl = new ymaps.control.ZoomControl({
			options: {
			    size: 'small',
			    float: 'none',
			    position: {
				bottom: 145,
				right: 10
			    }
			}
		    });
		// Пользователь сможет построить только автомобильный маршрут.
		routePanelControl.routePanel.options.set({
		    types: {auto: true}
		});
		
		// Если вы хотите задать неизменяемую точку "откуда", раскомментируйте код ниже.
		routePanelControl.routePanel.state.set({
		    fromEnabled: false,
		    from: 'Հանրապետության հրապարակ,Երևան'
		});
		myMap.controls.add(routePanelControl).add(zoomControl);
		
		// Получим ссылку на маршрут.
		routePanelControl.routePanel.getRouteAsync().then(function (route) {
		    
		    // Зададим максимально допустимое число маршрутов, возвращаемых мультимаршрутизатором.
		    route.model.setParams({results: 1}, true);
		    
				
		// Повесим обработчик на событие построения маршрута.
		    route.model.events.add('requestsuccess', function () {
			var activeRoute = route.getActiveRoute();
			if (activeRoute) {
			    // Получим протяженность маршрута.
			    var length = route.getActiveRoute().properties.get("distance"),
				// Вычислим стоимость доставки.
				price = calculate(Math.round(length.value / 1000)),
				
				// Создадим макет содержимого балуна маршрута.
				balloonContentLayout = ymaps.templateLayoutFactory.createClass('<span>Հեռավորությունը ' + length.text + '.</span><br/>' + '<span style="font-weight: bold; font-style: italic">Առաքման գինը կազմում է ' + price + ' դր.</span>');
			 
			   $(document).on('click', "#okok", function (e) {
               e.preventDefault();
					var valueAll = $('#cart-total-price').html();
					$('#checkout-form .errorlist').css({'display' : 'none'});
					$('#araqman_vjar').html(price);
				// 	valueAll = (parseInt(valueAll)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + (parseInt(price)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") 
					valueAll = parseInt(valueAll) + parseInt(price);
				// 	$('.final-sum').html((parseInt(valueAll) + parseInt(price)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " "))
			        $('.final-sum').html(valueAll)
			        $('.order_topay_curr').html(valueAll + '֏');
                    $('#id_all_total_price').val(valueAll);
                    $('#id_araqum').val(price);
				});	
					
				// 	if (price > 0) {
				// 	    
				// 		
				// 		$('.cart-summ-araqum').html(price);
				// 		$('#id_araqum').val(price);
				// 		
				// 	 ;
				// 	}
				// 	else {
				// 		$('#araqman_vjar').html('');
				// 		$('.cart-summ-araqum').html('');
				// 		$('#id_araqum').val('');
				// 		$('#checkout-form .errorlist').css({'display' : 'none'});
			
				
			    // Зададим этот макет для содержимого балуна.
			    route.options.set('routeBalloonContentLayout', balloonContentLayout);
				activeRoute.balloon.open();
			
				var points = route.getWayPoints();
				lastPoint = points.getLength() - 1;
				start_point = points.get(0).properties.get("coordinates");
				finish_point = points.get(lastPoint).properties.get("coordinates");
				 
				getAddress(routePanelControl.routePanel.state.get("to"));
				setmap_vals(price, length.text, finish_point);
			}
			else {
				$('#okok').hide();
				$('.confirm-address-user').hide();
			}
		    });
			
         //routePanelControl.routePanel.geolocate('to');	(atomat geolokacian voroshuma)
		$(document).on('click', '.ymaps-2-1-75-route-panel__clear', function () {
			$('#id_address').attr('');
			$('#address').attr('');
			$('.confirm-address-user').hide();
			
		});
		
		
		$(document).on('click', '#okok', function () {
			$('.confirm-address-user').show();
		});
		    
		});
		function getAddress(coords) {
		ymaps.geocode(coords).then(function (res) {
			var firstGeoObject = res.geoObjects.get(0);
			$('#address').attr('value',firstGeoObject.getAddressLine());
			$('#HiddenAddressVal').text(firstGeoObject.getAddressLine());
			
			$(document).on('click', '#okok', function () {
				$('#id_address').attr('value',firstGeoObject.getAddressLine());
			});
		
			
			$('#okok').show();
			$('.confirm-address-user').hide();
			coords = firstGeoObject.geometry.getCoordinates(), 
					
			// Область видимости геообъекта.
			bounds = firstGeoObject.properties.get('boundedBy');
			document.getElementById('latitude').value = coords[0];
			document.getElementById('longitude').value = coords[1];
		});
	}

	function setmap_vals(lat, lng, zoom) {
		document.getElementById('ymapleft').value = lat;
		document.getElementById('ymapright').value = lng;
		document.getElementById('ymapzoom').value = zoom;
	}

	function calculate(routeLength) {
		return Math.max(routeLength * DELIVERY_TARIFF, MINIMUM_COST);
	}
}