$(function() {
  window.Dataset = Backbone.Model.extend({
    idAttribute: '_id',

    defaults: {
      name: 'default name',
      insertedAt: 'default time'
    },

    parse: function(response) {
      response = response.dataset;
      return response;
    }
  });

  window.DatasetList = Backbone.Collection.extend({

    model: Dataset,
    url: '/datasets/',
    parse: function(response) {
      return response.datasets;
    }


  });

});
