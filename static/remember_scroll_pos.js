document.documentElement.style.scrollBehavior = 'auto';
        document.addEventListener("DOMContentLoaded", function(event) {
            var scrollpos = localStorage.getItem('scrollpos');
            if (scrollpos) {
                window.scrollTo({behavior: "instant"});
                window.scrollTo(0, scrollpos);
            }
        });

        window.onbeforeunload = function(e) {
            localStorage.setItem('scrollpos', window.scrollY);
        };




