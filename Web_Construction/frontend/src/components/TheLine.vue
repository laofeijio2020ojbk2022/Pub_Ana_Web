<template>
  <div ref="lineChart" style="width: 900px; height: 200px;"></div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';

export default {
  props: {
    timeData: {
      type: Object,
    }
  },
  name: 'TheLine',
  setup(props, { emit }) {
    const lineChart = ref(null);
    const chooseDate = ref('');

    onMounted(() => {
      drawChart(props.timeData);
    });

    watch(
      () => props.timeData,
      (newValue, oldValue) => {
        if (newValue !== oldValue) {
          drawChart(newValue);
        }
      }
    );

    watch(chooseDate, (newValue)  => {
      emit('send-data-date', newValue)
    });

    const drawChart = (data) => {
      const chartDom = lineChart.value;
      const myChart = echarts.init(chartDom);

      myChart.on('mousemove', function (params) {
        console.log(params)
      })

      const sortedData = Array.from(data.male).sort((a, b) => {
        return new Date(a.name) - new Date(b.name);
      });
      const sortedData2 = Array.from(data.female).sort((a, b) => {
        return new Date(a.name) - new Date(b.name);
      });
      const dates = sortedData.map((item) => item.name);
      const values = sortedData.map((item) => item.value);
      const values2 = sortedData2.map((item) => item.value);

      const option = {
        grid: {
          top: 5,
          left: '3%',
          right: '3%',
        },
        xAxis: {
          type: 'category',
          data: dates,
          // axisLabel: {
          //   interval: 0, // 强显示所有
          //  },
          show: true,
          splitNumber: Math.ceil(dates.length / 10), // 设置刻度分割个数，根据需要调整
        },
        yAxis: {
          type: 'value',
          show: false
        },
        dataZoom: [// 添加滑动条
          {
            type: 'slider',
            show: true,
            start: 0,
            end: 100
          }
        ],
        series: [
          {
            name:'女',
            data: values2,
            type: 'line',
            // stack: 'Total',
            lineStyle: {
              width: 0, // 设置折线宽度
            },
            symbolSize: 0, // 设置折线上数据点的大小
            itemStyle: {
              color: 'rgba(255, 105, 180, 1)', // 设置折线和数据点的颜色
            },
            areaStyle: { // 添加面积样式
              color: 'rgba(255, 105, 180, 1)',
              // color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ // 设置渐变颜色
              //   offset: 0,
              //   color: 'green' // 开始颜色
              // }, {
              //   offset: 1,
              //   color: 'green' // 结束颜色
              // }])
            }
          },
          {
            name: '男',
            data: values,
            type: 'line',
            // stack: 'Total',
            lineStyle: {
              width: 0, // 设置折线宽度
            },
            symbolSize: 0, // 设置折线上数据点的大小
            itemStyle: {
              color: 'rgba(65, 105, 225, 1)', // 设置折线和数据点的颜色
            },
            areaStyle: { // 添加面积样式
              color: 'rgba(65, 105, 225, 1)',
            }
          },
        ],
        tooltip: {
          trigger: 'axis', // 鼠标悬停会显示数据
          // axisPointer: {
          //   type: 'cross' // 设置指示器
          // }
          position: function (pos, params) {
            chooseDate.value = params[0].axisValue
          },
        },
        legend: {
          data: ['女', '男'], // 设置图例显示的名称
          top: 20, // 设置图例的位置
          right: 20,
          orient: 'vertical',
          textStyle: {
            color: '#333', // 设置图例文字颜色
          },
        },
      };

      myChart.setOption(option);
    };

    return {
      lineChart,
      chooseDate
    };
  }
};
</script>

<style scoped>
/* 这里可以添加样式 */
</style>
