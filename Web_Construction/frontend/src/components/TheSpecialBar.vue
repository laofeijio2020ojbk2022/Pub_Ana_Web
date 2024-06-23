<template>
  <div ref="chart" style="width: 900px; height: 400px;"></div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';

export default {
  name:'TheSpecialBar',
  props: {
    data: {
      type: Object,
    },
  },
  setup(props) {
    const chart = ref(null);
    const yAxisData = ['0-9岁', '10-19岁', '20-29岁', '30-39岁', '40-49岁', '50-59岁', '60-69岁', '70-79岁', '80-89岁', '90-99岁', '99岁以上'];

    const drawChart = () => {
      const chartDom = chart.value;
      const myChart = echarts.init(chartDom);

      const option = {
        label: {
          show: false,
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          orient: 'vertical',
          top: 10,
          right: 50,
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          top: '0%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          boundaryGap: [0, 0.01],
          // show: false,
        },
        yAxis: {
          // position: 'center',
          type: 'category',
          axisTick: {
            show: false
          },
          data: yAxisData,
        },
        series: [
          {
            name: '男',
            type: 'bar',
            stack: 'Total',
            itemStyle: {
              color: '#409EFF', // 蓝色部分颜色
            },
            data: props.data.male.map(item => ({
              'name': item.name,
              'value': -item.value,
            }))
          },
          {
            name: '女',
            type: 'bar',
            stack: 'Total',
            itemStyle: {
              color: '#F56C6C', // 红色部分颜色
            },
            data: props.data.female,
          }
        ]
      };

      myChart.setOption(option);
    };

    onMounted(() => {
      drawChart();
    });

    watch(() => props.data, () => {
      drawChart();
    });

    return { chart };
  },
};
</script>