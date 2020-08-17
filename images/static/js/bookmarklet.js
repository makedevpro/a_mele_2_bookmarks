(function () {
	let jquery_version = '3.3.1';
	let site_url = 'https://6b92a50991b1.ngrok.io/';
	let static_url = site_url + 'static';
	let min_width = 100;
	let min_height = 100;

	function bookmarklet(msg) {
		// Загрузка CSS-стилей.
		let css = jQuery('<link>');
		css.attr({
			rel: 'stylesheet',
			type: 'text/css',
			href: static_url + '/css/bookmarklet.css?r=' +
				Math.floor(Math.random()*9999999999999)
		});
		jQuery('head').append(css);

		// Загрузка HTML
		box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a>' +
			'<h1>Select an image to bookmark:</h1><div class="images">' +
			'</div></div>';
		jQuery('body').append(box_html);

		// ДОбавление скрытия букмарклета при нажатии на крестик.
		jQuery('#bookmarklet #close').click(function () {
			jQuery('#bookmarklet').remove();
		});

		jQuery.each(jQuery('img[src$="jpg"]'), function (index, image) {
			if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_height) {
				image_url = jQuery(image).attr('src');
				jQuery('#bookmarklet .images').append(
					'<a href="#"><img src="' + image_url + '" /></a>'
				);
			}
		});

		// Когда изображение выбрано, добавляем его в список сохраненных картинок на нашем сайте.
		jQuery('#bookmarklet .images a').click(function (e) {
			selected_image = jQuery(this).children('img').attr('src');
			// Скрываем букмарклет
			jQuery('#bookmarklet').hide();
			// Открываем новое окно с формой сохранения изображения.
			window.open(site_url + 'images/create/?url='
			+ encodeURIComponent(selected_image)
			+ '&title=' + encodeURIComponent(jQuery('title').text()),
				'_blank');
		});
	};

	// Проверка, подключена ли jQuery.
	if (typeof window.jQuery != 'undefined') {
		bookmarklet();
	}
	else {
		// Проверка, что атрибут $ окна не занят другим объектом
		let conflict = typeof window.$ != 'undefined';
		// Создание тега <script> с загрузкой jQuery.
		let script = document.createElement('script');
		script.src = '//ajax.googleapis.com/ajax/libs/jquery/' +
			jquery_version + '/jquery.min.js';
		// Добавление тега в блок <head> документа.
		document.head.appendChild(script);
		// Добавление возможности использовать несколько попыток для загрузки jQuery.
		let attemps = 15;
		(function () {
			// Проверка, подключена ли jQuery
			if (typeof window.jQuery == 'undefined') {
				if (--attemps > 0) {
					// Если не подключена, пытаемся снова загрузить
					window.setTimeout(arguments.callee, 250)
				}
				else {
					// Превышено число попыток загрузки jQuery, выводим сообщение.
					alert('An error occurred while loading jQuery')
				}
			} else {
				bookmarklet();
			}
		})();
	}
})();
