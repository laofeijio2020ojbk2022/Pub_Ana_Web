<template>
  <el-container>
    <div ref="barChart" style="width: 100%; height: 1000px;"></div>
  </el-container>
</template>

<script>
import * as echarts from 'echarts/core';
import { BarChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, GridComponent, DatasetComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import { use } from 'echarts/core';

use([TitleComponent, TooltipComponent, GridComponent, DatasetComponent, BarChart, CanvasRenderer]);

export default {
  name: 'TheHorizontalBar',
  props: {
    mapData: {
      type: Array,
      required: true
    },
    map2Data:{
      type: Object,
      required: true
    },
    dataModel:{
      type: Number,
      required: true
    }
  },
  data() {
    return {
      barChart: null
    };
  },
  mounted() {
    this.renderChart(this.mapData);
  },
  watch: {
    mapData(newValue) {
      // console.log('ok')
      // console.log(newValue)
      // Re-render the chart when chartData changes
      this.renderChart(newValue);
    },
    dataModel(newValue) {
      if(newValue === 1){
        this.renderChart(this.mapData)
      }else if(newValue === 2){
        this.renderChart(this.map2Data.male)
      }else if(newValue === 3){
        this.renderChart(this.map2Data.female)
      }
    }
  },
  methods: {
    renderChart(data) {
      if (!this.barChart) {
        this.barChart = echarts.init(this.$refs.barChart);
      }

      data.sort((a, b) => a.value - b.value); // Sort the data array based on 'value' in descending order

      const options = {
        grid: {
          top: 0,
          bottom: 30,
          left: '25%',
          right: '15%',
          // right: 100 // Increase the right margin to display data on top of bars
        },
        xAxis: { type: 'value', position: 'top', show: false},
        yAxis: {
          type: 'category',
          data: data.map(item => item.name),
          axisLabel: {
            interval: 0,  // Display all labels
            formatter: function (value) {
              // Shorten province names
              return value.length > 3 ? value.substring(0, 3) + '...' : value + '   ';
            }
          }
        },
        series: [{
          data: data.map(item => item.value.toFixed(1)),
          type: 'bar',
          label: {
            show: true,
            position: 'right', // Display values on top of the bars
            formatter: '{c}'  // Show the value on top of bars
          }
        }],
        color: ['#5C469C'],  // Customize the color of the bars
        backgroundColor: 'transparent',  // Set the background to transparent
      };

      this.barChart.setOption(options);
    }
  }
};
</script>
