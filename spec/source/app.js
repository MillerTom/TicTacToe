var TicTacToe = angular.module('TicTacToe', []);
TicTacToe.config(['$httpProvider', function($httpProvider, $interpolateProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';}
]);
TicTacToe.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});
TicTacToe.controller('TicTacCtrl', function($scope, $http){
  $scope.formData = {};
  $scope.play = function(cell_id){
    this.formData['cell_id'] = cell_id;
    $http.post('/play/', this.formData).
      success(function(data) {
        if (data['status'] != 'ok') {
          $scope.result = data['status'];
          $scope.again = true;
          $scope.checked0 = $scope.checked1 = $scope.checked2 = $scope.checked3 = $scope.checked4 =
            $scope.checked5 = $scope.checked6 = $scope.checked7 = $scope.checked8 = true;
        }
        $scope['status' + data['value']] = data['player'];
        $scope['checked' + data['value']] = true;
      }).
      error(function(){
        $scope.result = 'Error!';
      });
  };
  $scope.init = function(){
    $scope.play('');
  }
});
TicTacToe.controller('PlayerCtrl', function($scope, $http){
  $scope.formData = {};
  $scope.get_player_letter = function(letter){
    this.formData['player_letter'] = letter;
    $http.post('/get_player_letter/', this.formData).
      success(function(data){
        $scope.letter = data;
      }).
      error(function(){
      });
  };
  $scope.get_player_name = function(name){
    this.formData['player_name'] = name;
    $http.post('/get_player_name/', this.formData).
      success(function(data){
        $scope.player_name = data;
      }).
      error(function(data){
      });
  }
});