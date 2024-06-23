<template>
  <el-container style="position: relative;">
    <div class="map-model">
      <div><el-checkbox size="small" label="3D" v-model="model3D"></el-checkbox></div>
      <div><el-checkbox size="small" label="全部" v-model="all_flag"></el-checkbox></div>
      <div><el-checkbox size="small" label="男" v-model="male_flag"></el-checkbox></div>
      <div><el-checkbox size="small" label="女" v-model="female_flag"></el-checkbox></div>
    </div>
<!--    <div v-show="choose === 1" class="map-label">{{ selectedProvince }}</div>-->
    <div v-show="choose === 0" ref="chinaMap" style="height: 500px; width: 570px;"></div>
    <div v-show="choose === 1" ref="chinaMap3D" style="height: 500px; width: 570px; background-color: #000c17;"></div>
  </el-container>
</template>

<script>
import chinaJSON from '@/assets/china.json';
import * as echarts from 'echarts/core';
import 'echarts-gl'
import { onMounted, ref, watch } from 'vue';

import { GeoComponent, } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([GeoComponent, CanvasRenderer]);

export default {
  data () {
    return{
    }
  },
  props:{
    mapData:{
      type: Array,
      required: true
    },
    map2Data:{
      type: Object,
      required: true
    }
  },
  setup(props, { emit }) {
    const chinaMap = ref(null);
    const chinaMap3D = ref(null);
    const provinceMap = ref(null);
    const selectedProvince = ref('');
    const choose = ref(0);
    const all_flag = ref(true);
    const male_flag = ref(false);
    const female_flag = ref(false);
    const data_all = ref([]);
    const data_male = ref([]);
    const data_female = ref([]);
    const maxValue = ref(100);
    const myChart1 = ref(null);
    const model3D = ref(false);
    const mouseError = ref(null);

    // 监视all_flag的变化，更新data
    watch(all_flag, (newValue) => {
      console.log(newValue)
      if (model3D.value === true) {
        drawChina3D(chinaMap3D.value, props.mapData)
      }else{
        if (all_flag.value === true) {
          drawChina(chinaMap.value, props.mapData)
        }else if (male_flag.value === true) {
          drawChina(chinaMap.value, props.map2Data.male)
        }else if (female_flag.value === true) {
          drawChina(chinaMap.value, props.map2Data.female)
        }
      }
      if (all_flag.value === true) {
        emit('send-data', 1)
      }else if (male_flag.value === true) {
        emit('send-data', 2)
      }else if (female_flag.value === true) {
        emit('send-data', 3)
      }
    });

    watch(male_flag, (newValue) => {
      console.log(newValue)
      if (model3D.value === true) {
        drawChina3D(chinaMap3D.value, props.mapData)
      }else{
        if (all_flag.value === true) {
          drawChina(chinaMap.value, props.mapData)
        }else if (male_flag.value === true) {
          drawChina(chinaMap.value, props.map2Data.male)
        }else if (female_flag.value === true) {
          drawChina(chinaMap.value, props.map2Data.female)
        }
      }
      if (all_flag.value === true) {
        emit('send-data', 1)
      }else if (male_flag.value === true) {
        emit('send-data', 2)
      }else if (female_flag.value === true) {
        emit('send-data', 3)
      }
    });

    watch(female_flag, (newValue) => {
      console.log(newValue)
      if (model3D.value === true) {
        drawChina3D(chinaMap3D.value, props.mapData)
      }else{
        if (all_flag.value === true) {
          drawChina(chinaMap.value, props.mapData)
        }else if (male_flag.value === true) {
          drawChina(chinaMap.value, props.map2Data.male)
        }else if (female_flag.value === true) {
          drawChina(chinaMap.value, props.map2Data.female)
        }
      }
      if (all_flag.value === true) {
        emit('send-data', 1)
      }else if (male_flag.value === true) {
        emit('send-data', 2)
      }else if (female_flag.value === true) {
        emit('send-data', 3)
      }
    });

    watch(model3D, (newValue) => {
      console.log(newValue)
      if (newValue) {
        choose.value = 1
        drawChina3D(chinaMap3D.value, props.mapData)
      }else {
        choose.value = 0
      }
    });

    onMounted(() => {
      drawChina(chinaMap.value, props.mapData);
    });
    watch(() => props.mapData, (newVal) => {
      // console.log(newVal)
      drawChina(chinaMap.value, newVal);
      // drawProvince(provinceMap.value, newVal);
    });

    function getFormatter(name){
      let all = 0
      let male = 0
      let female = 0

      try {
        all = props.mapData.find(item => (item.name === name)).value
        // console.log(all)
        male = props.map2Data.male.find(item => (item.name === name)).value
        female = props.map2Data.female.find(item => (item.name === name)).value
      }catch (error) {
        mouseError.value = error
      }

      return `  ${ name }  \n  总热度：${ all }  \n  男：${ male }  \n  女：${ female }  `
    }

    function drawChina3D(chinaMapRef, data) {
      try {
        if (all_flag.value) {
          data_all.value = props.mapData.map(item => ({
            value: [...item.position, item.value/maxValue.value*30]
          }));
          console.log(data_all.value)
        } else {
          data_all.value = []; // 当flag为false时，清空data
        }
      }catch(error) {
        console.log('N0 Data')
      }

      try {
        if (male_flag.value) {
          data_male.value = props.map2Data.male.map(item => ({
            value: [...item.position, item.value / maxValue.value * 30]
          }));
          console.log(data_male.value)
        } else {
          data_male.value = []; // 当flag为false时，清空data
        }
      }catch(error) {
        console.log('No Male Data')
      }

      try {
        if (female_flag.value) {
          data_female.value = props.map2Data.female.map(item => ({
            value: [...item.position, item.value / maxValue.value * 30]
          }));
          console.log(data_female.value)
        } else {
          data_female.value = []; // 当flag为false时，清空data
        }
      }catch(error) {
        console.log('No Female Data')
      }

      maxValue.value = Math.max(...data.map(item => item.value));
      console.log(maxValue.value)

      const myChart = echarts.init(chinaMapRef);

      echarts.registerMap('china3D', chinaJSON)

      // myChart.on('mouseover',function (params) {
      //   if (params.componentType === 'series') {
      //     if (params.seriesType === 'map3D') {
      //       // 如果鼠标悬停在地图区域上
      //       console.log('悬停在地图上:', params);
      //       selectedProvince.value = params.name; // 获取悬停的省份名称
      //       // 执行相关操作，如显示相关信息等
      //     }
      //   }
      // })

      myChart.on('map3DSelected', function (params) {
        console.log(params)
      })

      // Rest of the configuration options...
      const option = {
        geo3D: {
          map: 'china3D',
          boxHeight: 20, // 设置地图厚度
          viewControl: {
            distance: 120,
            animation: true, // 是否开启动画
            zoomSensitivity: 0, // 禁止缩放
          },
          itemStyle: {
            color: '#034778', // 背景
            opacity: 1, //透明度
            borderWidth: .4, // 边框宽度
            borderColor: "#0cd8fd", // 边框颜色
          },
          label: {
            show: false,
          },
          emphasis: {
            itemStyle: {
              color: "#0cd8fd", //显示移入的区块变粉色
              opacity: 1, //透明度
            },
            label: {
              show: true,
              formatter: function(params) {
                // console.log(params);
                return getFormatter(params.name);
              },
              textStyle: {
                color: '#fff',
                fontSize: 16,
              },
              backgroundColor: 'rgba(255, 255, 255, 0.7)', // 设置白色背景颜色和透明度
              padding: 5, // 内边距
              borderWidth: 1, // 边框宽度
              borderColor: '#fff', // 边框颜色
              position: [10, 10], // 相对于容器的左上角偏移量
            }
          },
          light: { //光照阴影
            main: {
              color: '#fff', //光照颜色
              intensity: 1.2, //光照强度
              shadowQuality: 'high', //阴影亮度
              shadow: true, //是否显示阴影
              alpha: 50, //光照角度
              beta: -30, //光源方向
            },
            ambient: {
              intensity: 0.3//环境光的强度
            }//全局的环境光设置
          }
        },
        series: [
            {
              type: 'bar3D',
              coordinateSystem: 'geo3D',
              data: data_all.value,
              minHeight: 0,
              itemStyle: {
                color: '#0087f4', // 设置条形图的颜色
              },
              barSize: 1, // 设置条形图的尺寸
              shading: 'lambert', //三维图形的着色效果
              bevelSmoothness:1, //柱子倒角的光滑/圆润度，数值越大越光滑/圆润
              opacity: 1,
              bevelSize:0.1, //
              visible: false,
            },
            {
              type: 'bar3D',
              coordinateSystem: 'geo3D',
              data: data_male.value,
              minHeight: 0,
              itemStyle: {
                color: 'red', // 设置条形图的颜色
              },
              barSize: 1, // 设置条形图的尺寸
              shading: 'lambert', //三维图形的着色效果
              bevelSmoothness:1, //柱子倒角的光滑/圆润度，数值越大越光滑/圆润
              opacity: 1,
              bevelSize:0.1, //
              visible: false,
            },
            {
              type: 'bar3D',
              coordinateSystem: 'geo3D',
              data: data_female.value,
              minHeight: 0,
              itemStyle: {
                color: 'white', // 设置条形图的颜色
              },
              barSize: 1, // 设置条形图的尺寸
              shading: 'lambert', //三维图形的着色效果
              bevelSmoothness:1, //柱子倒角的光滑/圆润度，数值越大越光滑/圆润
              opacity: 1,
              bevelSize:0.1, //
              visible: false,
            }
        ],
      };

      myChart.setOption(option);
    }

    function drawChina(chinaMapRef, data) {
      maxValue.value = Math.max(...data.map(item => item.value));

      const myChart = echarts.init(chinaMapRef);

      echarts.registerMap('china', chinaJSON)

      // 省份点击事件
      myChart.on('click', (params) => {
        emit('send-data-province', params.name)
      });

      // Rest of the configuration options...
      const option = {
        geo: {
          map: 'china',
          // roam: true, //是否允许缩放，拖拽
          zoom: 1, //初始化大小
          //缩放大小限制
          scaleLimit: {
            min: 1, //最小
            max: 20, //最大
          },
          //设置中心点
          // center: [116.405285,39.904989],
          center: [105.97, 29.71],
          //省份地图添加背景
          regions: data.map(item => ({
            name: item.name,
            selected: false,
            label: {
              show: false,
              formatter: () => getFormatter(item.name),
              backgroundColor: 'rgba(255, 255, 255, 0.7)', // 设置白色背景颜色和透明度
              padding: 5, // 内边距
              borderWidth: 1, // 边框宽度
              borderColor: '#fff', // 边框颜色
              position: [10, 10], // 相对于容器的左上角偏移量
            },
            itemStyle: {
              areaColor: `rgba(12, 19, 79, ${item.value / maxValue.value})`, // Set area color based on the third value in the array
            },
          })),
          //高亮状态
          emphasis: {
            itemStyle: {
              areaColor: '#1af9e5',
              color: '#ffffff',
            },
          },
        },
        //配置属性
        series: {}
      };

      myChart.setOption(option);
    }

    return {
      chinaMap,
      chinaMap3D,
      provinceMap,
      selectedProvince,
      choose,
      all_flag,
      male_flag,
      female_flag,
      data_all,
      data_male,
      data_female,
      maxValue,
      myChart1,
      model3D,
    };
  },
  name: 'TheMap',
};
</script>

<style scoped>
.map-label {
    position: absolute;
    top: 0px; /* 距离容器顶部的距离 */
    left: 0px; /* 距离容器左侧的距离 */
    padding: 5px;
    background-color: rgba(255, 255, 255, 0.8);
    border: 1px solid #999;
}
.map-model {
    position: absolute;
    top: 0px;
    right: 10px;
    padding: 5px;
    background-color: rgba(255, 255, 255, 1);
    border: 1px solid #999;
}
</style>
