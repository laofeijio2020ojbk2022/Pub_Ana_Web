<template>
  <div>
    <img v-if="flag === -1" src="../assets/img/疑惑.png" alt="Image 4" style="width: 60%; border-radius: 50%">
    <img v-else-if="flag === 1" src="../assets/img/开心.png" alt="Image 1" style="width: 60%; border-radius: 50%">
    <img v-else-if="flag === 3" src="../assets/img/难过.png" alt="Image 3" style="width: 60%; border-radius: 50%">
    <img v-else src="../assets/img/一般.png" alt="Image 2" style="width: 60%; border-radius: 50%">
  </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  name: 'TheImg',
  props: {
    data:{
      type:Number,
    }
  },
  setup(props) {
    const flag = ref(-1); // 默认显示图2

    // 监听父组件传入的参数变化
    watch(() => props.data, (newValue) => {
      if (newValue < 0.4) {
        flag.value = 3; // 显示图1
      } else if (newValue > 0.6) {
        flag.value = 1; // 显示图3
      } else {
        flag.value = 2; // 显示图2
      }
    });

    return {
      flag,
    };
  }
};
</script>
