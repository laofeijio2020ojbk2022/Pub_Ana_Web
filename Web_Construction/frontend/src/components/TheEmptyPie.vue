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
  setup(props, { emit }) {
    const chart = ref(null);

    const drawChart = (data) => {
      const chartDom = chart.value;
      const myChart = echarts.init(chartDom);

      // 监听图例点击事件
      myChart.on('legendselectchanged', function (params) {
        const selected = params.selected;
        console.log(selected)
        const newOption = JSON.parse(JSON.stringify(myChart.getOption())); // 克隆当前选项

        // newOption.legend.show = false
        newOption.legend.show = true

        myChart.setOption(newOption); // 动态更新图表选项
      });

      myChart.on('click', function (params) {
        emit('send-topic-data', params.data.name)
      })

      const option = {
        legend: {
          orient: 'vertical',
          top: 10,
          left: 10,
          show: true,
          selectedMode: 'single',
          data: ['全部', '男', '女'],
        },
        // toolbox: {
        //   show: true,
        //   feature: {
        //     mark: { show: true },
        //     dataView: { show: true, readOnly: false },
        //     restore: { show: true },
        //     saveAsImage: { show: true }
        //   }
        // },
        series: [
          {
            name: '男',
            type: 'pie',
            radius: [50, 150],
            center: ['50%', '50%'],
            roseType: 'area',
            itemStyle: {
              borderRadius: 3
            },
            data: data.male
          },
          {
            name: '女',
            type: 'pie',
            radius: [50, 150],
            center: ['50%', '50%'],
            roseType: 'area',
            itemStyle: {
              borderRadius: 3
            },
            data: data.female
          },
          {
            name: '全部',
            type: 'pie',
            radius: [50, 150],
            center: ['50%', '50%'],
            roseType: 'area',
            itemStyle: {
              borderRadius: 3
            },
            data: data.all
          },
        ]
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