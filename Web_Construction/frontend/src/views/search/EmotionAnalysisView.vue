<template>
<el-container style="margin: 20px;">
  <el-header height="100px">

    <el-container style=
               "float: left;
                width: 28%;
                margin-left: 4%;
                margin-top: 30px;
                border-radius: 5px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                background-color: #f5f5f5;">
      <VueDatePicker v-model="date" range format="yyyy-MM-dd" style="width: 100%; height: 100%"/>
    </el-container>

    <el-container style=
                 "float: left;
                  width: 28%;
                  margin-left: 4%;
                  margin-top: 30px;
                  border-radius: 5px;
                  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                  background-color: #f5f5f5;">
      <el-button @click="get_data" style="width: 100%; height: 37px">查询热搜</el-button>
    </el-container>

    <el-container style=
                 "float: left;
                  width: 28%;
                  margin-left: 4%;
                  margin-top: 30px;
                  border-radius: 5px;
                  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                  background-color: #f5f5f5;">
      <el-button @click="get_emotion" style="width: 100%; height: 37px">开始分析</el-button>
    </el-container>
  </el-header>

  <el-container style="height: 500px; margin-bottom: 30px">
    <el-main style="float: left; width: 90%; height: 100%; margin-left: 3%; margin-right: 3%">
      <TheTable :data=dataList @selected-titles="handleSelectedTitles"></TheTable>
    </el-main>
  </el-container>

  <div style="margin-left: 5%; margin-right: 5%">
    <el-card style="margin-bottom: 50px">
      <h2 style="text-align: center; margin-top: 0px; margin-bottom: 0px">热门帖子情感分析结果</h2>
<!--      <span>算法1：hot_title + hot_post</span>-->
    </el-card>
    <el-space :size="23">
      <el-card style="width: 290px; height: 290px">
<!--        <ThePie :data="data1.result1" style="width: 270px; height: 270px"></ThePie>-->
        <el-container style="margin: 50px;">
          <el-progress type="dashboard" :percentage="Math.floor(img1 * 100)" :width="150" :color="customColors">
            <template #default="{ percentage }">
              <span class="percentage-value">{{ percentage }}%</span>
              <span class="percentage-label">情感指数</span>
            </template>
          </el-progress>
        </el-container>
      </el-card>
      <el-card style="width: 290px; height: 290px; --el-card-padding: 0px;">
        <el-container style="width: 290px; height: 290px">
          <ThePie :data="data1.emo1" style="width: 290px; height: 290px"></ThePie>
        </el-container>
      </el-card>
      <el-card style="width: 290px; height: 290px;">
        <TheImg :data="img1" style="width: 260px; height: 260px; margin: 45px"></TheImg>
      </el-card>
    </el-space>
  </div>

  <div style="margin: 50px 5%;">
    <el-card style="margin-bottom: 50px">
      <h2 style="text-align: center; margin-top: 0px; margin-bottom: 0px">热门评论情感分析结果</h2>
<!--      算法2：hot_title + hot_post + hot_comment-->
    </el-card>
    <el-space :size="23">
      <el-card style="width: 290px; height: 290px">
<!--        <ThePie :data="data2.result2" style="width: 270px; height: 270px;"></ThePie>-->
        <el-container style="margin: 50px;">
          <el-progress type="dashboard" :percentage="Math.floor(img2 * 100)" :width="150" :color="customColors">
            <template #default="{ percentage }">
              <span class="percentage-value">{{ percentage }}%</span>
              <span class="percentage-label">情感指数</span>
            </template>
          </el-progress>
        </el-container>
      </el-card>
      <el-card style="width: 290px; height: 290px;  --el-card-padding: 0px;">
        <el-container style="width: 290px; height: 290px">
          <ThePie :data="data2.emo2" style="width: 290px; height: 290px"></ThePie>
        </el-container>
      </el-card>
      <el-card style="width: 290px; height: 290px;">
        <TheImg :data="img2" style="width: 260px; height: 260px; margin: 45px"></TheImg>
      </el-card>
    </el-space>
  </div>

</el-container>
</template>

<script>
import VueDatePicker from '@vuepic/vue-datepicker';
import {onMounted, ref} from "vue";
import '@vuepic/vue-datepicker/dist/main.css'
import TheTable from '@/components/TheTable.vue'
import ThePie from '@/components/ThePie.vue'
import TheImg from "@/components/TheImg.vue";

export default{
  data () {
    return{
      time_start:'2023-12-29',
      time_end:'2023-12-30',

      dataList: [],
      data1:{
        emo1:[],
        result1:[],
      },
      data2:{
        emo2:[],
        result2:[],
      },
      img1:0.5,
      img2:0.5,
    }
  },
  components:{
    TheImg,
    VueDatePicker,
    TheTable,
    ThePie,
  },
  methods:{
    async get_data() {
      this.back = 'waitting...'
      this.time_start = this.change_date(this.date[0])
      this.time_end = this.change_date(this.date[1])
      this.$axios.get('http://127.0.0.1:8000/api/title?time_start='
          + this.time_start + '&time_end=' + this.time_end)
          .then((response) => {
            const res = response.data
            // console.log(res)
            this.dataList = res
            // console.log(this.time_start)
            // console.log(this.time_end)
          })
    },
    async get_emotion() {
      // console.log(this.selectedTitles)
      this.back = 'waitting...'
      this.$axios.get('http://127.0.0.1:8000/api/emotion?titles=' + this.selectedTitles)
          .then((response) => {
            const res = response.data
            // console.log(res)
            this.data1 = res.data1
            this.data2 = res.data2
            // console.log(this.data1)
            // console.log(this.data2)
            this.img1 = this.data1.result1[0].value
            this.img2 = this.data2.result2[0].value
          })
    },
    change_date(date) {
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Adding leading zero if necessary
      const day = date.getDate().toString().padStart(2, '0'); // Adding leading zero if necessary
      return `${year}-${month}-${day}`;
    },
  },
  setup() {
    const date = ref();
    const selectedTitles = ref('');

    const customColors = [
      { color: '#13294b', percentage: 10 },   // 深蓝色
      { color: '#1a305f', percentage: 14 },
      { color: '#213373', percentage: 18 },
      { color: '#293a87', percentage: 22 },
      { color: '#31429b', percentage: 26 },
      { color: '#3b6ab9', percentage: 30 },  // 浅蓝色
      { color: '#538de5', percentage: 34 },
      { color: '#6eadd4', percentage: 38 },
      { color: '#90c2eb', percentage: 42 },
      { color: '#b6d6ef', percentage: 46 },
      { color: '#ffd700', percentage: 50 },  // 黄色
      { color: '#ffcc00', percentage: 54 },  // 亮橙色
      { color: '#ff5733', percentage: 58 },  // 深橙红色
      { color: '#ff3333', percentage: 62 },  // 鲜红色
      { color: '#ff1a1a', percentage: 66 },  // 红色
      { color: '#e60000', percentage: 70 },  // 深红色
      { color: '#cc0000', percentage: 74 },
      { color: '#b30000', percentage: 78 },
      { color: '#990000', percentage: 82 },
      { color: '#800000', percentage: 86 },  // 深棕色
    ];




    const handleSelectedTitles = (titles) => {
      // 在父组件中处理接收到的选中的title数据
      // console.log('selected-titles:', titles);
      // 可以进行相应的处理

      // 或者将选中的title保存到父组件中
      selectedTitles.value = titles;
    };

    // For demo purposes assign range from the current date
    onMounted(() => {
      const startDate = new Date();
      const endDate = new Date(new Date().setDate(startDate.getDate()));

      date.value = [startDate, endDate];
    });

    return {
      date,
      selectedTitles,
      handleSelectedTitles,
      customColors,
    };
  },
}
</script>

<style scoped>
.percentage-value {
  display: block;
  margin-top: 20px;
  font-size: 38px;
}
.percentage-label {
  display: block;
  margin-top: 15px;
  font-size: 15px;
}
</style>