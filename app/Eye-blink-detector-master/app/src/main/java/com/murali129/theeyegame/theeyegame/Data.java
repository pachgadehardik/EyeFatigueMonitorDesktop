package com.murali129.theeyegame.theeyegame;

import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;
import java.io.Serializable;

public class Data implements Serializable {
    public LineGraphSeries<DataPoint> getLg() {
        return lg;
    }

    public void setLg(LineGraphSeries<DataPoint> lg) {
        this.lg = lg;
    }

    public LineGraphSeries<DataPoint> lg;

}
