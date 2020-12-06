package com.krikorherlopian.tictactoe_minimax;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.animation.AnimationUtils;
import android.widget.ImageView;
import android.widget.TextView;

import com.bumptech.glide.Glide;

public class MainActivity extends AppCompatActivity {

    int count = 0;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView textView = (TextView)findViewById(R.id.text);
        textView.startAnimation(AnimationUtils.loadAnimation(this, R.anim.anim));
        runHandler();
    }

    public void runHandler(){
        Handler handler = new Handler(Looper.getMainLooper());
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                ImageView im = (ImageView)findViewById(R.id.src);
                switch (count){
                    case 0:
                        Glide.with(MainActivity.this).load(R.drawable.frame0).placeholder(R.drawable.frame0).into(im);
                        break;
                    case 1:
                        Glide.with(MainActivity.this).load(R.drawable.frame1).placeholder(R.drawable.frame0).into(im);
                        break;
                    case 2:
                        Glide.with(MainActivity.this).load(R.drawable.frame2).placeholder(R.drawable.frame1).into(im);
                        break;
                    case 3:
                        Glide.with(MainActivity.this).load(R.drawable.frame3).placeholder(R.drawable.frame2).into(im);
                        break;
                    case 4:
                        Glide.with(MainActivity.this).load(R.drawable.frame4).placeholder(R.drawable.frame3).into(im);
                        break;
                    case 5:
                        Glide.with(MainActivity.this).load(R.drawable.frame5).placeholder(R.drawable.frame4).into(im);
                        break;
                    case 6:
                        Intent i = new Intent(getApplicationContext(), GameActivity.class);
                        startActivity(i);
                        finish();
                        break;
                }
                runHandler();
                count++;
            }
        },1000);
    }
}