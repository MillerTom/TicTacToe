describe('Angular Test', function(){
  beforeEach(module('TicTacToe'));
  describe('Game Scope Check', function(){
    it('should check scopes at game page.', inject(function($controller){
      var scope = {},
      ctrl =$controller('TicTacCtrl', { $scope: scope });
      expect(scope.formData).toBeDefined();
      expect(scope.init).toBeDefined();
      expect(scope.play).toBeDefined();
    }));
  });
  describe('Home Scope Check', function(){
    it('should check scopes at home page.', inject(function($controller){
      var scope = {},
      ctrl =$controller('PlayerCtrl', { $scope: scope });
      expect(scope.formData).toBeDefined();
      expect(scope.get_player_letter).toBeDefined();
      expect(scope.get_player_name).toBeDefined();
    }));
  });
  describe('Get Player Info', function(){
    var $httpBackend, $rootScope, createController;

    beforeEach(inject(function($injector) {
      // Set up the mock http service responses
      $httpBackend = $injector.get('$httpBackend');
      $rootScope = $injector.get('$rootScope');
      var $controller = $injector.get('$controller');

      createController = function() {
        return $controller('PlayerCtrl', {'$scope' : $rootScope });
      };
    }));
    afterEach(function() {
      $httpBackend.verifyNoOutstandingExpectation();
      $httpBackend.verifyNoOutstandingRequest();
    });
    it('should get user letter.', function() {
      var controller = createController();

      $rootScope.formData = {'player_letter': 'X'};
      $httpBackend.expectPOST('/get_player_letter/', $rootScope.formData).respond(200, 'X');
      $rootScope.get_player_letter('X');
      expect($rootScope.letter).toBe('X');
      $httpBackend.flush();

    });
    it('should get player type.', function() {
      var controller = createController();

      $rootScope.formData = {'player_name': 'human'};
      $httpBackend.expectPOST('/get_player_name/', $rootScope.formData).respond(200, 'human');
      $rootScope.get_player_name('human');
      expect($rootScope.player_name).toBe('human');
      $httpBackend.flush();

    });
  });
});