from django.shortcuts import render
from django.http import StreamingHttpResponse
import engine
from .engine import Game
import json


def new_board():
    n_board = ['', ] * 9
    return n_board


def get_current_board(request):
    """
    Get current board or create a new board.
    """
    if 'board' not in request.session:
        request.session['board'] = new_board()

    return request.session['board']


def clear_board(request):
    """
    Remove the existing board, if there is one, and set a new one
    """
    if 'board' in request.session:
        del request.session['board']


def get_player_letter(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        request.session['player_letter'] = req['player_letter']

        return StreamingHttpResponse(request.session['player_letter'])
    return request.session['player_letter']


def get_player_name(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        request.session['player_name'] = req['player_name']

        return StreamingHttpResponse(request.session['player_name'])
    return request.session['player_name']


def cell_list():
    """ create a list of cell labels for the board"""
    _cell_list = []
    for row in ['top', 'middle', 'bottom']:
        for col in ['left', 'center', 'right']:
            _cell_list.append(col + ' ' + row)
    return _cell_list


def board(request):
    # always start with a new board
    board_list = new_board()
    request.session['board'] = new_board()
    cells = cell_list()
    my_board = [zip(cells[:3], board_list[:3], range(0, 3)),
                zip(cells[3:6], board_list[3:6], range(3, 6)),
                zip(cells[6:], board_list[6:], range(6, 9))]
    context = {'board': my_board,
               'player_letter': request.session['player_letter'],
               'computer_letter': engine.OPPONENTS[request.session['player_letter']],
               'player_name': request.session['player_name']}
    return render(request, 'tictactoe.html', context)


def json_response(status='ok', value=None, player=None):
    response = {'status': status}
    if value is not None:
        response['value'] = value
    if player is not None:
        response['player'] = player

    response = StreamingHttpResponse(json.dumps(response), content_type='application/json')
    return response


def play(request):
    # Get game info
    req = json.loads(request.body)
    cell = req['cell_id']
    player_name = request.session['player_name']
    player_letter = request.session['player_letter']
    current_board = get_current_board(request)

    # Initialise engine
    game = Game(player_letter)

    if player_name == 'computer':
        move = game.get_computer_move(current_board)
        current_board = game.make_move(current_board, game.computer_letter, move)
        if game.is_winner(current_board, game.computer_letter):
            game._is_over = True
            return json_response(status='Computer Won', value=move, player=game.computer_letter.lower())
        else:
            if game.is_board_full(current_board):
                game._is_over = True
                return json_response(status='Tie', value=move, player=game.computer_letter.lower())
            else:
                request.session['board'] = current_board
                request.session['player_name'] = 'human'
                return json_response(value=move, player=game.computer_letter.lower())

    else:
        move = int(cell)
        current_board = game.make_move(current_board, player_letter, move)
        if game.is_winner(current_board, player_letter):
            game._is_over = True
            return json_response(status='Player Won', value=move, player=player_letter.lower())
        else:
            if game.is_board_full(current_board):
                game._is_over = True
                return json_response(status='Tie', value=move, player=player_letter.lower())
            else:
                request.session['board'] = current_board
                request.session['player_name'] = 'computer'
                return play(request)


def home(request):
    clear_board(request)
    return render(request, 'home.html')