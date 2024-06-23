// PieChart.vue
<template>
  <div ref="chart" style="width: 100px; height: 100px"></div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';

export default {
  name:'ThePie',
  props: {
    data: {
      type: Array,
      default: () => [],
    },
  },
  setup(props) {
    const chart = ref(null);

    const drawChart = (data) => {
      const chartDom = chart.value;
      const myChart = echarts.init(chartDom);

      let colors;
      if (props.data.length === 3) {
        colors = ['#ff6666', '#ffff66', '#6666ff'];
      } else {
        colors = ['#0C134F', '#404591', '#5964C7', '#7D95E5', '#A9C7FF', '#FFDD89', '#FFB85A', '#FF9453', '#DD6B4B', '#D14D72'];
      }

      const sortedData = data.sort((a, b) => {
        const aVal = parseInt(a.name.split('-')[0]);
        const bVal = parseInt(b.name.split('-')[0]);
        return aVal - bVal;
      });

      const option = {
        color: colors,
        tooltip: {
          trigger: 'item',
          formatter: '{b} : {c} ({d}%)',
          position: function (pos, params, dom, rect, size) {
            return {
              top: pos[1] - size.contentSize[1] / 2,
              left: pos[0] - size.contentSize[0] / 2
            };
          }
        },
        series: [
          {
            name: '占比',
            type: 'pie',
            radius: '50%',
            center: ['50%', '50%'],
            data: sortedData.map((item, index) => {
              return { value: item.value, name: item.name, itemStyle: { color: colors[index] } };
            }),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              },
            },
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
