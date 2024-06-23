<template>
  <div ref="chart" style="width: 100%; height: 100%"></div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';

export default {
  props: {
    data: {
      type: Object,
    },
  },
  setup(props) {
    const chart = ref(null);

    const drawChart = (data) => {
      let male_data = 50
      let female_data = 50
      try{
        male_data = (data.male[0].value/(data.male[0].value + data.female[0].value)*100).toFixed(2)
      }catch(error){
        console.log(error)
      }
      try{
        female_data = (data.female[0].value/(data.male[0].value + data.female[0].value)*100).toFixed(2)
      }catch(error){
        console.log(error)
      }

      const chartDom = chart.value;
      const myChart = echarts.init(chartDom);

      const option = {
        tooltip: {
          trigger: 'axis', // 鼠标悬停时触发
          axisPointer: {
            type: 'shadow' // 设置指示器类型
          }
        },
        grid: {
          containLabel: true,
          left: '0%',
          right: '0%',
          top: '0%',
          bottom: '0%',
        },
        xAxis: {
          type: 'value',
          max: 100, // x 轴最大值
          axisLine: {
            show: false, // 隐藏 x 轴线
          },
          axisTick: {
            show: false, // 隐藏刻度线
          },
          axisLabel: {
            show: false, // 隐藏标签
          },
          splitLine: {
            show: false, // 隐藏分割线
          },
        },
        yAxis: {
          type: 'category',
          data: ['活跃度指数对比'],
          axisLine: {
            show: false, // 隐藏 y 轴线
          },
          axisTick: {
            show: false, // 隐藏刻度线
          },
          axisLabel: {
            show: false, // 隐藏标签
          },
        },
        series: [
          {
            name: '男',
            type: 'bar',
            stack: 'total',
            barWidth: 20, // 条形图宽度
            itemStyle: {
              color: '#409EFF', // 蓝色部分颜色
              barBorderRadius: [10, 10, 10, 10],
            },
            data: [male_data], // 蓝色部分的数值，这里假设为 60
          },
          {
            name: '女',
            type: 'bar',
            stack: 'total',
            itemStyle: {
              color: '#F56C6C', // 红色部分颜色
              barBorderRadius: [10, 10, 10, 10],
            },
            data: [female_data], // 红色部分的数值，这里假设为 40
          },
        ],
      };


      myChart.setOption(option);
    };

    const updateChart = (newData) => {
      drawChart(newData);
    };

    onMounted(() => {
      drawChart(props.data);
    });

    watch(() => props.data, (newData, oldData) => {
      if (newData !== oldData) {
          updateChart(newData);
        }
    });

    return {
      chart,
      updateChart, // Expose the updateChart method to parent component
    };
  },
};
</script>

<style scoped>

</style>