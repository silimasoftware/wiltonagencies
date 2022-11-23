(function ($) {
    'use strict';
    var Hero = {
        getDebounce: function (func, wait, immediate) {
            var timeout;
            return function () {
                var context = this,
                    args = arguments;
                var later = function () {
                    timeout = null;
                    if (!immediate) func.apply(context, args);
                };
                var callNow = immediate && !timeout;
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
                if (callNow) func.apply(context, args);
            };
        },

        getSlick: function ($method) {
            $('[data-init="slick"]').each(function () {
                var el = $(this);

                var breakpointsWidth = {
                    tn: 319,
                    xs: 479,
                    ss: 519,
                    sm: 767,
                    md: 991,
                    lg: 1199
                };

                var slickDefault = {
                    dots: true,
                    arrows: false,

                    fade: true,
                    infinite: true,
                    autoplay: true,
                    pauseOnHover: true,
                    speed: 1000,
                    adaptiveHeight: true,

                    slidesToShow: 1,
                    slidesToScroll: 1,

                    mobileFirst: true
                };

                // Merge settings.
                var settings = $.extend(slickDefault, el.data());
                delete settings.init;

                // Build breakpoints.
                if (settings.breakpoints) {
                    var _responsive = [];
                    var _breakpoints = settings.breakpoints;

                    var buildBreakpoints = function buildBreakpoints(key, show, scroll) {
                        if (show !== 0) {
                            if (breakpointsWidth[key] != 991 && breakpointsWidth[key] != 1199) {
                                _responsive.push({
                                    breakpoint: breakpointsWidth[key],
                                    settings: {
                                        slidesToShow: parseInt(show),
                                        slidesToScroll: 1
                                    }
                                });
                            } else {
                                _responsive.push({
                                    breakpoint: breakpointsWidth[key],
                                    settings: {
                                        slidesToShow: parseInt(show),
                                        slidesToScroll: 1,
                                        dots: false,
                                        arrows: true
                                    }
                                });
                            }
                        };
                    };

                    if ((typeof _breakpoints === 'undefined' ? 'undefined' : _typeof(_breakpoints)) === "object") {
                        $.each(_breakpoints, buildBreakpoints);
                    }

                    delete settings.breakpoints;
                    settings.responsive = _responsive;
                };

                if ($method != 'unslick') el.slick(settings);
                else el.slick($method);
            });
        },

        getYoutubePlayer: function () {
            $('[data-video="youtube"]').each(function () {
                $(this).YTPlayer({
                    showControls: false
                });
            });
        },

        getVimeoPlayer: function () {
            $('[data-video="vimeo"]').each(function () {
                $(this).vimeo_player({
                    showControls: false
                });
            });
        },

        init: function () {
            var self = this;

            // Call functions use debounce resize function
            var resizeDebounce = self.getDebounce(function () {}, 250);

            self.getSlick();
            self.getYoutubePlayer();
            self.getVimeoPlayer();

            window.addEventListener('resize', resizeDebounce);
        }
    };

    $(document).ready(function () {
        Hero.init();
        var animationDelay = 2500,
            //loading bar effect
            barAnimationDelay = 3800,
            barWaiting = barAnimationDelay - 3000, //3000 is the duration of the transition on the loading bar - set in the scss/css file
            //letters effect
            lettersDelay = 50,
            //type effect
            typeLettersDelay = 150,
            selectionDuration = 500,
            typeAnimationDelay = selectionDuration + 800,
            //clip effect
            revealDuration = 600,
            revealAnimationDelay = 1500;

        initHeadline();


        function initHeadline() {
            //insert <i> element for each letter of a changing word
            singleLetters($('.hero-section.letters').find('.title__effect'));
            //initialise headline animation
            animateHeadline($('.hero-section'));
        }

        function singleLetters($words) {
            $words.each(function () {
                var word = $(this),
                    letters = word.text().split(''),
                    selected = word.hasClass('is-visible');

                var newLetters = letters.join('');
                word.html(newLetters).css('opacity', 1);
            });
        }

        function animateHeadline($headlines) {
            var duration = animationDelay;
            $headlines.each(function () {
                var headline = $(this);

                if (headline.hasClass('clip')) {
                    var spanWrapper = headline.find('.hero-section__words'),
                        newWidth = spanWrapper.width() + 10
                    spanWrapper.css('width', newWidth);
                } else {
                    //assign to .hero-section__words the width of its longest word
                    var words = headline.find('.hero-section__words .title__effect'),
                        width = 0;

                    $(window).load(function () {
                        words.each(function () {
                            var wordWidth = $(this).width();
                            if (wordWidth > width) width = wordWidth;
                        });

                        headline.find('.hero-section__words').css('width', width);
                    });
                };

                //trigger animation
                setTimeout(function () {
                    hideWord(headline.find('.is-visible').eq(0))
                }, duration);
            });
        }

        function hideWord($word) {
            var nextWord = takeNext($word);

            if ($word.parents('.hero-section').hasClass('clip')) {
                $word.parents('.hero-section__words').animate({
                    width: '2px'
                }, revealDuration, function () {
                    switchWord($word, nextWord);
                    showWord(nextWord);
                });

            } else {
                switchWord($word, nextWord);
                setTimeout(function () {
                    hideWord(nextWord)
                }, animationDelay);
            }
        }

        function showWord($word, $duration) {
            if ($word.parents('.hero-section').hasClass('clip')) {
                $word.parents('.hero-section__words').animate({
                    'width': $word.width() + 10
                }, revealDuration, function () {
                    setTimeout(function () {
                        hideWord($word)
                    }, revealAnimationDelay);
                });
            }
        }

        function hideLetter($letter, $word, $bool, $duration) {
            $letter.removeClass('in').addClass('out');

            if (!$letter.is(':last-child')) {
                setTimeout(function () {
                    hideLetter($letter.next(), $word, $bool, $duration);
                }, $duration);
            } else if ($bool) {
                setTimeout(function () {
                    hideWord(takeNext($word))
                }, animationDelay);
            }

            if ($letter.is(':last-child') && $('html').hasClass('no-csstransitions')) {
                var nextWord = takeNext($word);
                switchWord($word, nextWord);
            }
        }

        function showLetter($letter, $word, $bool, $duration) {
            $letter.addClass('in').removeClass('out');

            if (!$letter.is(':last-child')) {
                setTimeout(function () {
                    showLetter($letter.next(), $word, $bool, $duration);
                }, $duration);
            } else {
                if (!$bool) {
                    setTimeout(function () {
                        hideWord($word)
                    }, animationDelay)
                }
            }
        }

        function takeNext($word) {
            return (!$word.is(':last-child')) ? $word.next() : $word.parent().children().eq(0);
        }

        function takePrev($word) {
            return (!$word.is(':first-child')) ? $word.prev() : $word.parent().children().last();
        }

        function switchWord($oldWord, $newWord) {
            $oldWord.removeClass('is-visible').addClass('is-hidden');
            $newWord.removeClass('is-hidden').addClass('is-visible');
        }
    });

})(jQuery);