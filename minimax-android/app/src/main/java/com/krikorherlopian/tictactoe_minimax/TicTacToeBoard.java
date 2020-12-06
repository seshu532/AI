package com.krikorherlopian.tictactoe_minimax;

import java.util.ArrayList;
import java.util.List;


public class TicTacToeBoard {

    List<Point> pointsAvailable;
    int[][] ticTacToeBoard = new int[3][3];
    List<ScoresAndPoints> scores;
    int rowColSize = 3;

    public void placeAMove(Point point, int player) {
        ticTacToeBoard[point.x][point.y] = player;
    }


    public List<Point> getStates() {
        pointsAvailable = new ArrayList<>();
        for (int row = 0; row < rowColSize; ++row) {
            for (int col = 0; col < rowColSize; ++col) {
                if (ticTacToeBoard[row][col] == 0) {
                    pointsAvailable.add(new Point(row, col));
                }
            }
        }
        return pointsAvailable;
    }


    public int returnMaximum(List<Integer> list) {
        int max = Integer.MIN_VALUE;
        int index = -1;
        for (int i = 0; i < list.size(); ++i) {
            if (list.get(i) > max) {
                max = list.get(i);
                index = i;
            }
        }
        return list.get(index);
    }

    public Point perfectMove() {
        int maximum = -100000;
        int best = -1;

        for (int val = 0; val < scores.size(); ++val) {
            if (maximum < scores.get(val).score) {
                maximum = scores.get(val).score;
                best = val;
            }
        }

        return scores.get(best).point;
    }

    public void callMinimaxFunction(int depth, int turn){
        scores = new ArrayList<>();
        minimax(depth, turn);
    }

    public int minimax(int depth, int turn) {
        List<Point> pointsAvailable = getStates();
        List<Integer> scoreList = new ArrayList<>();
        if(ticTacToeBoard[0][2] == ticTacToeBoard[1][1] && ticTacToeBoard[0][2] == ticTacToeBoard[2][0] && ticTacToeBoard[0][2] == 2)
            return -1;
        else if (ticTacToeBoard[0][0] == ticTacToeBoard[1][1] && ticTacToeBoard[0][0] == ticTacToeBoard[2][2] && ticTacToeBoard[0][0] == 2) {
            return -1;
        }
        else if (ticTacToeBoard[0][2] == ticTacToeBoard[1][1] && ticTacToeBoard[0][2] == ticTacToeBoard[2][0] && ticTacToeBoard[0][2] == 1) {
            return +1;
        }
        else if(ticTacToeBoard[0][0] == ticTacToeBoard[1][1] && ticTacToeBoard[0][0] == ticTacToeBoard[2][2] && ticTacToeBoard[0][0] == 1)
            return +1;

        for (int i = 0; i < rowColSize; ++i) {
            if (((ticTacToeBoard[i][0] == ticTacToeBoard[i][1] && ticTacToeBoard[i][0] == ticTacToeBoard[i][2] && ticTacToeBoard[i][0] == 1)
                    || (ticTacToeBoard[0][i] == ticTacToeBoard[1][i] && ticTacToeBoard[0][i] == ticTacToeBoard[2][i] && ticTacToeBoard[0][i] == 1))) {
                return +1;
            }
            if ((ticTacToeBoard[i][0] == ticTacToeBoard[i][1] && ticTacToeBoard[i][0] == ticTacToeBoard[i][2] && ticTacToeBoard[i][0] == 2)
                    || (ticTacToeBoard[0][i] == ticTacToeBoard[1][i] && ticTacToeBoard[0][i] == ticTacToeBoard[2][i] && ticTacToeBoard[0][i] == 2)) {
                return -1;
            }
        }

        if (pointsAvailable.isEmpty()){
            return 0;
        }

        for (int i = 0; i < pointsAvailable.size(); ++i) {
            Point point = pointsAvailable.get(i);
            if (turn == 2) {
                placeAMove(point, 2);
                scoreList.add(minimax(depth + 1, 1));
            }
            else if (turn == 1) {
                placeAMove(point, 1);
                int currentScore = minimax(depth + 1, 2);
                scoreList.add(currentScore);

                if (depth == 0)
                    scores.add(new ScoresAndPoints(currentScore, point));

            }
            ticTacToeBoard[point.x][point.y] = 0;
        }
        if(turn == 1)
            return returnMaximum(scoreList);
        else
            return returnMinimum(scoreList);

    }


    public int returnMinimum(List<Integer> list) {
        int min = Integer.MAX_VALUE;
        int index = -1;
        for (int i = 0; i < list.size(); ++i) {
            if (list.get(i) < min) {
                min = list.get(i);
                index = i;
            }
        }
        return list.get(index);
    }

}