package com.murali129.theeyegame.theeyegame;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;
import com.jjoe64.graphview.series.Series;

import java.util.HashMap;

public class GraphyActivity extends AppCompatActivity {
    private Data data;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_graphy);
        GraphView graph = (GraphView) findViewById(R.id.graph);
        Intent intent = getIntent();
        HashMap<Integer, Long> hashMap = (HashMap<Integer, Long>)intent.getSerializableExtra("value");
        LineGraphSeries<DataPoint> series = new LineGraphSeries<>(generate(hashMap));
        graph.addSeries(series);
    }

    private DataPoint[] generate(HashMap<Integer,Long> hashMap) {
        DataPoint []dt = new DataPoint[hashMap.size()];
        int i=0;
        for (Integer key : hashMap.keySet()){
            dt[i]=new DataPoint(hashMap.get(key),key);
            i++;
        }

        return dt;
    }
}
