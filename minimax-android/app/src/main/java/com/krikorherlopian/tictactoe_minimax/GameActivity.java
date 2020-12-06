package com.krikorherlopian.tictactoe_minimax;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;

public class GameActivity extends AppCompatActivity {

    char [][] myBoard;
    TicTacToeBoard ticTacToeBoard = new TicTacToeBoard();
    int sizeGrid;
    TextView textViewTurn;
    TableLayout gameBoard;
    char turn;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.game);

        gameBoard = (TableLayout) findViewById(R.id.mainBoard);
        textViewTurn = (TextView) findViewById(R.id.turn);

        sizeGrid = Integer.parseInt(getString(R.string.size_of_board));
        myBoard = new char [sizeGrid][sizeGrid];


        resetBoard();
        textViewTurn.setText("Turn: "+turn);

        for(int i = 0; i< gameBoard.getChildCount(); i++){
            TableRow row = (TableRow) gameBoard.getChildAt(i);
            for(int j = 0; j<row.getChildCount(); j++){
                TextView tv = (TextView) row.getChildAt(j);
                tv.setText(R.string.none);
                tv.setOnClickListener(Move(i, j, tv));
            }
        }

        Button reset_btn = (Button) findViewById(R.id.reset);
        reset_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent current = getIntent();
                finish();
                startActivity(current);
            }
        });
    }

    protected void resetBoard(){
        turn = 'X';
        for(int row = 0; row< sizeGrid; row++){
            for(int col = 0; col < sizeGrid; col++){
                myBoard[row][col] = ' ';
            }
        }
    }

    protected int gameStatus(){
        for(int i = 0; i< sizeGrid; i++){
            if(checkRowEquality(i,'X'))
                return 1;
            if(checkColumnEquality(i, 'X'))
                return 1;
            if(checkRowEquality(i,'O'))
                return 2;
            if(checkColumnEquality(i,'O'))
                return 2;
            if(checkDiagonal('X'))
                return 1;
            if(checkDiagonal('O'))
                return 2;
        }

        boolean boardFull = true;
        for(int i = 0; i< sizeGrid; i++){
            for(int j = 0; j< sizeGrid; j++){
                if(myBoard[i][j]==' ')
                    boardFull = false;
            }
        }
        if(boardFull)
            return -1;
        else return 0;
    }

    protected boolean checkDiagonal(char player){
        int count1 = 0,count2 = 0;
        for(int i = 0; i< sizeGrid; i++)
            if(myBoard[i][i]==player)
                count1++;
        for(int i = 0; i< sizeGrid; i++)
            if(myBoard[i][sizeGrid -1-i]==player)
                count2++;
        if(count1 == sizeGrid || count2== sizeGrid)
            return true;
        else return false;
    }



    protected boolean cellSet(int row, int column){
        if(myBoard[row][column]==' ')
            return false;
        else
            return true;
    }


    View.OnClickListener Move(final int row, final int column, final TextView textView){

        return new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                playUser(row,column,textView);
            }
        };
    }

    public void playUser(int row, int column,final TextView tv){
        try{
            if(cellSet(row,column) == false) {
                myBoard[row][column] = turn;

                if (turn == 'O') {
                    setText(getResources().getString(R.string.O) ,'X',tv,false);
                }
                else if (turn == 'X') {
                    setText(getResources().getString(R.string.X) ,'O',tv,false);
                }
                if(gameStatus() == -1){
                    setText("This game ends in a draw" ,turn,textViewTurn,true);
                }
                else if (gameStatus() == 0) {
                    setText("Player X turn" ,turn,textViewTurn,false);
                }
                else{
                    setText(turn+" Loses!Sorry!" ,turn,textViewTurn,true);
                }
                playComputer(row, column);
            }
            else{
                textViewTurn.setText(textViewTurn.getText()+" Choose an Empty Call");
            }
        }
        catch (Exception e){}
    }

    public void playComputer(int row, int column){
        try{
            Point userMove = new Point(row, column);
            ticTacToeBoard.placeAMove(userMove, 2);
            ticTacToeBoard.callMinimaxFunction(0, 1);
            for (ScoresAndPoints pas : ticTacToeBoard.scores) {
                System.out.println("Point: " + pas.point + " Score: " + pas.score);
            }
            ticTacToeBoard.placeAMove(ticTacToeBoard.perfectMove(), 1);
            if(cellSet(ticTacToeBoard.perfectMove().x, ticTacToeBoard.perfectMove().y) == false) {

                myBoard[ticTacToeBoard.perfectMove().x][ticTacToeBoard.perfectMove().y] = turn;
                TableLayout tblLayout = (TableLayout)findViewById(R.id.mainBoard);

                TableRow r = (TableRow)tblLayout.getChildAt(ticTacToeBoard.perfectMove().x);
                TextView tv= (TextView) r.getChildAt(ticTacToeBoard.perfectMove().y);


                if (turn == 'O') {
                    setText(getResources().getString(R.string.O) ,'X',tv,false);
                }
                else if (turn == 'X') {
                    setText(getResources().getString(R.string.X) ,'O',tv,false);
                }
                if(gameStatus() == -1){
                    setText("This game ends in a draw" ,turn,textViewTurn,true);
                }
                else if (gameStatus() == 0) {
                    setText("Player X turn" ,turn,textViewTurn,false);
                }
                else{
                    setText(turn+" Loses!Sorry!" ,turn,textViewTurn,true);
                }
            }

        }
        catch (Exception e){}
    }

    public void setText(String text, Character ox, TextView tv, boolean endMatch ){
        tv.setText(text);
        turn = ox;
        if(endMatch)
            endMatch();
    }
    protected void endMatch(){
        for(int i = 0; i< gameBoard.getChildCount(); i++){
            TableRow row = (TableRow) gameBoard.getChildAt(i);
            for(int j = 0; j<row.getChildCount(); j++){
                TextView tv = (TextView) row.getChildAt(j);
                tv.setOnClickListener(null);
            }
        }
    }

    protected boolean checkColumnEquality(int c, char player){
        int count=0;
        for(int row = 0; row< sizeGrid; row++){
            if(myBoard[row][c]==player)
                count = count + 1;
        }

        if(sizeGrid != count)
            return false;
        else
            return true;
    }
    protected boolean checkRowEquality(int row, char player){
        int count = 0;
        for(int col = 0; col < sizeGrid; col++){
            if(myBoard[row][col]==player){
                count = count + 1;
            }
        }

        if(count != sizeGrid)
            return false;
        else
            return true;
    }


}