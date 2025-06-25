/* Review Frontend JavaScript */

odoo.define('review_feedback_system.frontend', function (require) {
'use strict';

var core = require('web.core');
var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');

var _t = core._t;

// Review Rating Widget
publicWidget.registry.ReviewRating = publicWidget.Widget.extend({
    selector: '.rating-input',
    events: {
        'change input[type="radio"]': '_onRatingChange',
        'mouseenter .rating-label': '_onRatingHover',
        'mouseleave .rating-input': '_onRatingLeave',
    },

    _onRatingChange: function (ev) {
        var rating = $(ev.currentTarget).val();
        this._updateRatingDisplay(rating);
    },

    _onRatingHover: function (ev) {
        var $label = $(ev.currentTarget);
        var rating = $label.prev('input').val();
        this._updateRatingDisplay(rating, true);
    },

    _onRatingLeave: function (ev) {
        var selectedRating = this.$('input[type="radio"]:checked').val();
        this._updateRatingDisplay(selectedRating || 0);
    },

    _updateRatingDisplay: function (rating, isHover) {
        var $labels = this.$('.rating-label');
        $labels.each(function (index) {
            var $label = $(this);
            var labelRating = $label.prev('input').val();
            if (labelRating <= rating) {
                $label.addClass('text-warning').removeClass('text-muted');
            } else {
                $label.addClass('text-muted').removeClass('text-warning');
            }
        });
    },
});

// Review Voting Widget
publicWidget.registry.ReviewVoting = publicWidget.Widget.extend({
    selector: '.review-voting',
    events: {
        'click .vote-btn': '_onVoteClick',
    },

    _onVoteClick: function (ev) {
        ev.preventDefault();
        var $btn = $(ev.currentTarget);
        var reviewId = $btn.data('review-id');
        var helpful = $btn.data('helpful');

        if ($btn.hasClass('voted')) {
            return; // Already voted
        }

        this._submitVote(reviewId, helpful, $btn);
    },

    _submitVote: function (reviewId, helpful, $btn) {
        var self = this;
        
        ajax.jsonRpc('/review/vote', 'call', {
            review_id: reviewId,
            helpful: helpful
        }).then(function (result) {
            if (result.error) {
                self._showNotification(result.error, 'danger');
            } else {
                self._updateVoteDisplay(result, $btn);
                self._showNotification(_t('Thank you for your feedback!'), 'success');
            }
        }).catch(function (error) {
            self._showNotification(_t('An error occurred. Please try again.'), 'danger');
        });
    },

    _updateVoteDisplay: function (result, $btn) {
        var $container = $btn.closest('.review-voting');
        var $helpfulBtn = $container.find('[data-helpful="true"]');
        var $helpfulCount = $helpfulBtn.find('.helpful-count');
        
        // Update counts
        $helpfulCount.text(result.helpfulness_count);
        
        // Mark as voted
        $btn.addClass('voted').prop('disabled', true);
        
        // Update summary text
        var summaryText = result.helpfulness_count + ' out of ' + result.total_votes + ' found this helpful';
        $container.find('.text-muted').text(summaryText);
    },

    _showNotification: function (message, type) {
        var $notification = $('<div class="alert alert-' + type + ' alert-dismissible fade show" role="alert">' +
            message +
            '<button type="button" class="close" data-dismiss="alert">' +
            '<span>&times;</span>' +
            '</button>' +
            '</div>');
        
        $('body').prepend($notification);
        
        setTimeout(function () {
            $notification.alert('close');
        }, 5000);
    },
});

// Product Reviews Loader
publicWidget.registry.ProductReviews = publicWidget.Widget.extend({
    selector: '#product-reviews-container',

    start: function () {
        this._super.apply(this, arguments);
        this._loadProductReviews();
    },

    _loadProductReviews: function () {
        var self = this;
        var productId = this.$el.data('product-id');
        
        if (!productId) {
            return;
        }

        ajax.jsonRpc('/reviews/api/stats', 'call', {
            product_id: productId
        }).then(function (stats) {
            self._renderProductReviews(stats);
        }).catch(function (error) {
            self.$el.html('<div class="text-center text-muted">Unable to load reviews</div>');
        });
    },

    _renderProductReviews: function (stats) {
        var template = `
            <div class="product-reviews-summary mb-4">
                <div class="row">
                    <div class="col-md-6">
                        <div class="average-rating">
                            <h4>${stats.average_rating.toFixed(1)} <small class="text-muted">out of 5</small></h4>
                            <div class="rating-stars">
                                ${this._renderRatingStars(stats.average_rating)}
                            </div>
                            <p class="text-muted">${stats.total_reviews} reviews</p>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="rating-breakdown">
                            ${this._renderRatingBreakdown(stats.rating_breakdown)}
                        </div>
                    </div>
                </div>
            </div>
            <div class="text-center">
                <a href="/reviews/product/${stats.product_id}" class="btn btn-outline-primary">
                    View All Reviews
                </a>
                <a href="/review/submit?product_id=${stats.product_id}" class="btn btn-primary ml-2">
                    Write a Review
                </a>
            </div>
        `;
        
        this.$el.html(template);
    },

    _renderRatingStars: function (rating) {
        var stars = '';
        for (var i = 1; i <= 5; i++) {
            if (i <= rating) {
                stars += '<i class="fa fa-star text-warning"></i>';
            } else if (i - 0.5 <= rating) {
                stars += '<i class="fa fa-star-half-o text-warning"></i>';
            } else {
                stars += '<i class="fa fa-star-o text-muted"></i>';
            }
        }
        return stars;
    },

    _renderRatingBreakdown: function (breakdown) {
        var html = '';
        for (var i = 5; i >= 1; i--) {
            var count = breakdown[i + '_star'] || 0;
            var percentage = breakdown.total > 0 ? (count / breakdown.total * 100) : 0;
            html += `
                <div class="rating-breakdown-item d-flex align-items-center mb-1">
                    <span class="rating-label">${i} star</span>
                    <div class="progress flex-grow-1 mx-2" style="height: 8px;">
                        <div class="progress-bar bg-warning" style="width: ${percentage}%"></div>
                    </div>
                    <span class="rating-count text-muted">${count}</span>
                </div>
            `;
        }
        return html;
    },
});

// Review Form Validation
publicWidget.registry.ReviewForm = publicWidget.Widget.extend({
    selector: '.review-form',
    events: {
        'submit': '_onFormSubmit',
        'input .form-control': '_onInputChange',
    },

    _onFormSubmit: function (ev) {
        if (!this._validateForm()) {
            ev.preventDefault();
            this._showValidationErrors();
        }
    },

    _onInputChange: function (ev) {
        var $input = $(ev.currentTarget);
        this._clearValidationError($input);
    },

    _validateForm: function () {
        var isValid = true;
        var self = this;

        // Check required fields
        this.$('.form-control[required]').each(function () {
            var $field = $(this);
            if (!$field.val().trim()) {
                self._addValidationError($field, _t('This field is required'));
                isValid = false;
            }
        });

        // Check email format
        var $email = this.$('input[type="email"]');
        if ($email.length && $email.val()) {
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test($email.val())) {
                this._addValidationError($email, _t('Please enter a valid email address'));
                isValid = false;
            }
        }

        // Check rating selection
        var $rating = this.$('input[name="rating"]:checked');
        if (!$rating.length) {
            this._addValidationError(this.$('.rating-input'), _t('Please select a rating'));
            isValid = false;
        }

        return isValid;
    },

    _addValidationError: function ($field, message) {
        $field.addClass('is-invalid');
        var $feedback = $field.siblings('.invalid-feedback');
        if (!$feedback.length) {
            $feedback = $('<div class="invalid-feedback"></div>');
            $field.after($feedback);
        }
        $feedback.text(message);
    },

    _clearValidationError: function ($field) {
        $field.removeClass('is-invalid');
        $field.siblings('.invalid-feedback').remove();
    },

    _showValidationErrors: function () {
        var $firstError = this.$('.is-invalid').first();
        if ($firstError.length) {
            $firstError.focus();
            $('html, body').animate({
                scrollTop: $firstError.offset().top - 100
            }, 500);
        }
    },
});

// Review Search and Filter
publicWidget.registry.ReviewSearch = publicWidget.Widget.extend({
    selector: '.reviews-search-form',
    events: {
        'submit': '_onSearchSubmit',
        'change .filter-control': '_onFilterChange',
    },

    _onSearchSubmit: function (ev) {
        // Let the form submit naturally
    },

    _onFilterChange: function (ev) {
        // Auto-submit when filters change
        this.$el.submit();
    },
});

// Review Image Gallery
publicWidget.registry.ReviewImageGallery = publicWidget.Widget.extend({
    selector: '.review-attachments',
    events: {
        'click img': '_onImageClick',
    },

    _onImageClick: function (ev) {
        var $img = $(ev.currentTarget);
        var src = $img.attr('src');
        var alt = $img.attr('alt') || 'Review Image';
        
        this._showImageModal(src, alt);
    },

    _showImageModal: function (src, alt) {
        var modalHtml = `
            <div class="modal fade" id="imageModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${alt}</h5>
                            <button type="button" class="close" data-dismiss="modal">
                                <span>&times;</span>
                            </button>
                        </div>
                        <div class="modal-body text-center">
                            <img src="${src}" class="img-fluid" alt="${alt}">
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        var $modal = $(modalHtml);
        $('body').append($modal);
        $modal.modal('show');
        
        $modal.on('hidden.bs.modal', function () {
            $modal.remove();
        });
    },
});

// Initialize all widgets when DOM is ready
$(document).ready(function () {
    // Auto-submit search form with delay
    var searchTimer;
    $('.reviews-search-input').on('input', function () {
        clearTimeout(searchTimer);
        var $form = $(this).closest('form');
        searchTimer = setTimeout(function () {
            $form.submit();
        }, 500);
    });

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function (e) {
        e.preventDefault();
        var target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 100
            }, 500);
        }
    });

    // Auto-hide alerts
    $('.alert').each(function () {
        var $alert = $(this);
        if (!$alert.hasClass('alert-permanent')) {
            setTimeout(function () {
                $alert.fadeOut();
            }, 5000);
        }
    });
});

return {
    ReviewRating: publicWidget.registry.ReviewRating,
    ReviewVoting: publicWidget.registry.ReviewVoting,
    ProductReviews: publicWidget.registry.ProductReviews,
    ReviewForm: publicWidget.registry.ReviewForm,
    ReviewSearch: publicWidget.registry.ReviewSearch,
    ReviewImageGallery: publicWidget.registry.ReviewImageGallery,
};

});
