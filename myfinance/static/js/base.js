current_url = document.URL

array = current_url.split('/')
current_page = array[array.length-1]

if(current_page==='home' || current_page===''){
    $('.nav-link.active').toggleClass('active');
    var element = $('#navbarScroll > ul.navbar-nav.me-auto.my-2.my-lg-0.navbar-nav-scroll > li:nth-child(1) > a');
    element.toggleClass('active');
}

if(current_page==='profile'){
    $('.nav-link.active').toggleClass('active');
    var element = $('#navbarScroll > ul.navbar-nav.me-auto.my-2.my-lg-0.navbar-nav-scroll > li:nth-child(2) > a');
    element.toggleClass('active');
}

if(current_page==='login'){
    $('.nav-link.active').toggleClass('active');
    var element = $('#navbarScroll > ul.navbar-nav.flex-row.flex-wrap.ms-md-auto > li:nth-child(1) > a');
    element.toggleClass('active');
}

if(current_page==='register'){
    $('.nav-link.active').toggleClass('active');
    var element = $('#navbarScroll > ul.navbar-nav.flex-row.flex-wrap.ms-md-auto > li:nth-child(2) > a');
    element.toggleClass('active');
}

if(current_page==='new'){
    $('.nav-link.active').toggleClass('active');
    var element = $('#navbarScroll > ul.navbar-nav.flex-row.flex-wrap.ms-md-auto > li:nth-child(1) > a');
    element.toggleClass('active');
}
