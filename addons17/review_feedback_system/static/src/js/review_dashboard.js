/* Review Dashboard JavaScript */

odoo.define('review_feedback_system.dashboard', function (require) {
'use strict';

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var rpc = require('web.rpc');
var web_client = require('web.web_client');
var Widget = require('web.Widget');

var QWeb = core.qweb;
var _t = core._t;

// Review Dashboard Action
var ReviewDashboard = AbstractAction.extend({
    template: 'ReviewDashboard',
    events: {
        'click .review-stat-card': '_onStatCardClick',
        'click .refresh-dashboard': '_onRefreshClick',
        'change .dashboard-filter': '_onFilterChange',
    },

    init: function (parent, context) {
        this._super(parent, context);
        this.dashboardData = {};
        this.filters = {
            period: 'month',
            category: null,
            product: null,
        };
    },

    willStart: function () {
        var self = this;
        return this._super().then(function () {
            return self._loadDashboardData();
        });
    },

    start: function () {
        var self = this;
        return this._super().then(function () {
            self._renderDashboard();
            self._setupCharts();
        });
    },

    _loadDashboardData: function () {
        var self = this;
        return rpc.query({
            model: 'review.feedback',
            method: 'get_dashboard_data',
            args: [this.filters],
        }).then(function (data) {
            self.dashboardData = data;
        });
    },

    _renderDashboard: function () {
        var self = this;
        
        // Render stat cards
        this._renderStatCards();
        
        // Render recent reviews
        this._renderRecentReviews();
        
        // Render moderation queue
        this._renderModerationQueue();
        
        // Render trends
        this._renderTrends();
    },

    _renderStatCards: function () {
        var data = this.dashboardData;
        var $container = this.$('.dashboard-stats');
        
        var stats = [
            {
                title: _t('Total Reviews'),
                value: data.total_reviews || 0,
                icon: 'fa-star',
                color: 'primary',
                action: 'all_reviews'
            },
            {
                title: _t('Pending Moderation'),
                value: data.pending_moderation || 0,
                icon: 'fa-clock-o',
                color: 'warning',
                action: 'pending_moderation'
            },
            {
                title: _t('Published Reviews'),
                value: data.published_reviews || 0,
                icon: 'fa-check-circle',
                color: 'success',
                action: 'published_reviews'
            },
            {
                title: _t('Average Rating'),
                value: (data.average_rating || 0).toFixed(1),
                icon: 'fa-star-half-o',
                color: 'info',
                action: 'rating_analysis'
            }
        ];

        var cardsHtml = '';
        stats.forEach(function (stat) {
            cardsHtml += `
                <div class="col-md-3">
                    <div class="card stat-card stat-card-${stat.color}" data-action="${stat.action}">
                        <div class="card-body text-center">
                            <i class="fa ${stat.icon} fa-2x mb-2"></i>
                            <h3 class="stat-value">${stat.value}</h3>
                            <p class="stat-title">${stat.title}</p>
                        </div>
                    </div>
                </div>
            `;
        });

        $container.html('<div class="row">' + cardsHtml + '</div>');
    },

    _renderRecentReviews: function () {
        var reviews = this.dashboardData.recent_reviews || [];
        var $container = this.$('.recent-reviews-list');
        
        if (reviews.length === 0) {
            $container.html('<div class="text-center text-muted py-4">No recent reviews</div>');
            return;
        }

        var reviewsHtml = '';
        reviews.forEach(function (review) {
            var statusClass = {
                'draft': 'secondary',
                'submitted': 'warning',
                'approved': 'success',
                'rejected': 'danger',
                'archived': 'dark'
            }[review.state] || 'secondary';

            var rating = '';
            for (var i = 1; i <= 5; i++) {
                rating += '<i class="fa fa-star' + (i <= review.rating_value ? ' text-warning' : '-o text-muted') + '"></i>';
            }

            reviewsHtml += `
                <div class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                        <h6 class="mb-1">${review.title}</h6>
                        <small class="text-muted">${review.create_date}</small>
                    </div>
                    <div class="mb-1">
                        <div class="rating mb-1">${rating}</div>
                        <p class="mb-1">${review.content.substring(0, 100)}${review.content.length > 100 ? '...' : ''}</p>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">By ${review.customer_name || review.partner_name || 'Anonymous'}</small>
                        <span class="badge badge-${statusClass}">${review.state}</span>
                    </div>
                </div>
            `;
        });

        $container.html('<div class="list-group">' + reviewsHtml + '</div>');
    },

    _renderModerationQueue: function () {
        var queue = this.dashboardData.moderation_queue || [];
        var $container = this.$('.moderation-queue-list');
        
        if (queue.length === 0) {
            $container.html('<div class="text-center text-muted py-4">No reviews pending moderation</div>');
            return;
        }

        var queueHtml = '';
        queue.forEach(function (review) {
            var rating = '';
            for (var i = 1; i <= 5; i++) {
                rating += '<i class="fa fa-star' + (i <= review.rating_value ? ' text-warning' : '-o text-muted') + '"></i>';
            }

            queueHtml += `
                <div class="card mb-3">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="flex-grow-1">
                                <h6 class="card-title">${review.title}</h6>
                                <div class="rating mb-2">${rating}</div>
                                <p class="card-text">${review.content.substring(0, 150)}${review.content.length > 150 ? '...' : ''}</p>
                                <small class="text-muted">
                                    By ${review.customer_name || review.partner_name || 'Anonymous'} 
                                    on ${review.create_date}
                                </small>
                            </div>
                            <div class="ml-3">
                                <button class="btn btn-success btn-sm approve-review" data-review-id="${review.id}">
                                    <i class="fa fa-check"></i> Approve
                                </button>
                                <button class="btn btn-danger btn-sm reject-review ml-1" data-review-id="${review.id}">
                                    <i class="fa fa-times"></i> Reject
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        $container.html(queueHtml);
        
        // Bind moderation actions
        this._bindModerationActions();
    },

    _renderTrends: function () {
        var trends = this.dashboardData.trends || {};
        var $container = this.$('.trends-container');
        
        // Render trend summary
        var trendsHtml = `
            <div class="row">
                <div class="col-md-4">
                    <div class="trend-item">
                        <h5>${trends.reviews_this_month || 0}</h5>
                        <p class="text-muted">Reviews This Month</p>
                        <small class="text-${trends.reviews_trend > 0 ? 'success' : 'danger'}">
                            <i class="fa fa-arrow-${trends.reviews_trend > 0 ? 'up' : 'down'}"></i>
                            ${Math.abs(trends.reviews_trend || 0)}% vs last month
                        </small>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="trend-item">
                        <h5>${(trends.avg_rating_this_month || 0).toFixed(1)}</h5>
                        <p class="text-muted">Avg Rating This Month</p>
                        <small class="text-${trends.rating_trend > 0 ? 'success' : 'danger'}">
                            <i class="fa fa-arrow-${trends.rating_trend > 0 ? 'up' : 'down'}"></i>
                            ${Math.abs(trends.rating_trend || 0).toFixed(1)} vs last month
                        </small>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="trend-item">
                        <h5>${trends.response_rate || 0}%</h5>
                        <p class="text-muted">Response Rate</p>
                        <small class="text-info">
                            Business responses to reviews
                        </small>
                    </div>
                </div>
            </div>
        `;
        
        $container.html(trendsHtml);
    },

    _setupCharts: function () {
        this._setupRatingChart();
        this._setupTimelineChart();
    },

    _setupRatingChart: function () {
        var chartData = this.dashboardData.rating_distribution || {};
        var $canvas = this.$('#ratingChart');
        
        if (!$canvas.length || !window.Chart) {
            return;
        }

        var ctx = $canvas[0].getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['5 Stars', '4 Stars', '3 Stars', '2 Stars', '1 Star'],
                datasets: [{
                    data: [
                        chartData.five_star || 0,
                        chartData.four_star || 0,
                        chartData.three_star || 0,
                        chartData.two_star || 0,
                        chartData.one_star || 0
                    ],
                    backgroundColor: [
                        '#28a745',
                        '#20c997',
                        '#ffc107',
                        '#fd7e14',
                        '#dc3545'
                    ]
                }]
            },
            options: {
                responsive: true,
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Rating Distribution'
                }
            }
        });
    },

    _setupTimelineChart: function () {
        var timelineData = this.dashboardData.timeline || [];
        var $canvas = this.$('#timelineChart');
        
        if (!$canvas.length || !window.Chart || timelineData.length === 0) {
            return;
        }

        var ctx = $canvas[0].getContext('2d');
        var labels = timelineData.map(function (item) { return item.date; });
        var reviews = timelineData.map(function (item) { return item.count; });
        var ratings = timelineData.map(function (item) { return item.avg_rating; });

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Reviews Count',
                    data: reviews,
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    yAxisID: 'y-axis-1'
                }, {
                    label: 'Average Rating',
                    data: ratings,
                    borderColor: '#ffc107',
                    backgroundColor: 'rgba(255, 193, 7, 0.1)',
                    yAxisID: 'y-axis-2'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    yAxes: [{
                        type: 'linear',
                        display: true,
                        position: 'left',
                        id: 'y-axis-1',
                    }, {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        id: 'y-axis-2',
                        gridLines: {
                            drawOnChartArea: false,
                        },
                    }]
                },
                title: {
                    display: true,
                    text: 'Reviews Timeline'
                }
            }
        });
    },

    _bindModerationActions: function () {
        var self = this;
        
        this.$('.approve-review').on('click', function (e) {
            e.preventDefault();
            var reviewId = $(this).data('review-id');
            self._moderateReview(reviewId, 'approve');
        });

        this.$('.reject-review').on('click', function (e) {
            e.preventDefault();
            var reviewId = $(this).data('review-id');
            self._moderateReview(reviewId, 'reject');
        });
    },

    _moderateReview: function (reviewId, action) {
        var self = this;
        
        rpc.query({
            model: 'review.feedback',
            method: action === 'approve' ? 'action_approve' : 'action_reject',
            args: [[reviewId]],
        }).then(function () {
            self.displayNotification({
                type: 'success',
                title: _t('Success'),
                message: _t('Review has been ') + (action === 'approve' ? _t('approved') : _t('rejected')),
            });
            self._loadDashboardData().then(function () {
                self._renderDashboard();
            });
        }).catch(function (error) {
            self.displayNotification({
                type: 'danger',
                title: _t('Error'),
                message: _t('An error occurred while processing the review'),
            });
        });
    },

    _onStatCardClick: function (e) {
        var action = $(e.currentTarget).data('action');
        this._navigateToAction(action);
    },

    _onRefreshClick: function (e) {
        e.preventDefault();
        var self = this;
        this._loadDashboardData().then(function () {
            self._renderDashboard();
        });
    },

    _onFilterChange: function (e) {
        var $filter = $(e.currentTarget);
        var filterType = $filter.data('filter');
        var filterValue = $filter.val();
        
        this.filters[filterType] = filterValue;
        
        var self = this;
        this._loadDashboardData().then(function () {
            self._renderDashboard();
        });
    },

    _navigateToAction: function (actionType) {
        var actionMapping = {
            'all_reviews': 'review_feedback_system.action_review_feedback',
            'pending_moderation': 'review_feedback_system.action_review_moderation',
            'published_reviews': 'review_feedback_system.action_review_published',
            'rating_analysis': 'review_feedback_system.action_review_analytics',
        };

        var actionName = actionMapping[actionType];
        if (actionName) {
            this.do_action(actionName);
        }
    },
});

// Register the dashboard action
core.action_registry.add('review_feedback_system.dashboard', ReviewDashboard);

// Review Quick Actions Widget
var ReviewQuickActions = Widget.extend({
    template: 'ReviewQuickActions',
    events: {
        'click .quick-approve': '_onQuickApprove',
        'click .quick-reject': '_onQuickReject',
        'click .quick-respond': '_onQuickRespond',
    },

    init: function (parent, reviewId) {
        this._super(parent);
        this.reviewId = reviewId;
    },

    _onQuickApprove: function (e) {
        e.preventDefault();
        this._moderateReview('approve');
    },

    _onQuickReject: function (e) {
        e.preventDefault();
        this._moderateReview('reject');
    },

    _onQuickRespond: function (e) {
        e.preventDefault();
        this._openResponseDialog();
    },

    _moderateReview: function (action) {
        var self = this;
        
        rpc.query({
            model: 'review.feedback',
            method: action === 'approve' ? 'action_approve' : 'action_reject',
            args: [[this.reviewId]],
        }).then(function () {
            self.trigger_up('reload');
        });
    },

    _openResponseDialog: function () {
        var self = this;
        this.do_action({
            type: 'ir.actions.act_window',
            res_model: 'review.response.wizard',
            view_mode: 'form',
            view_type: 'form',
            views: [[false, 'form']],
            target: 'new',
            context: {
                default_review_id: this.reviewId,
            },
        });
    },
});

return {
    ReviewDashboard: ReviewDashboard,
    ReviewQuickActions: ReviewQuickActions,
};

});
