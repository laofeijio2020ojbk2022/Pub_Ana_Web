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
    <el-main style="float: left; width: 90%; margin-left: 3%; margin-right: 3%">
      <TheTable :data=dataList @selected-titles="handleSelectedTitles"></TheTable>
    </el-main>
  </el-container>

  <div style="margin-left: 5%; margin-right: 5%">
    <el-card style="margin-bottom: 50px">
      <h2 style="text-align: center; margin-top: 0px; margin-bottom: 0px">热门帖子热搜热词分析结果</h2>
    </el-card>
    <el-container style="--el-main-padding: 0px; height: 450px; margin-bottom: 30px">
      <el-main style="float: left; width: 20%;"></el-main>
      <el-main style="float: left;
                    width: 60%;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                    background-color: #f5f5f5;">
        <img src="../../../../the_wordcloud1.png" style="width: 100%; height: 97%;">
      </el-main>
      <el-main style="float: left; width: 20%;"></el-main>
    </el-container>
  </div>

  <div style="margin-left: 5%; margin-right: 5%; margin-top: 20px">
    <el-card style="margin-bottom: 50px">
      <h2 style="text-align: center; margin-top: 0px; margin-bottom: 0px">热门评论热搜热词分析结果</h2>
    </el-card>
    <el-container style="--el-main-padding: 0px; height: 450px; margin-bottom: 30px">
      <el-main style="float: left; width: 20%;"></el-main>
      <el-main style="float: left;
                    width: 60%;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                    background-color: #f5f5f5;">
        <img src="../../../../the_wordcloud2.png" style="width: 100%; height: 97%;">
      </el-main>
      <el-main style="float: left; width: 20%;"></el-main>
    </el-container>
  </div>

</el-container>
</template>

<script>
import VueDatePicker from "@vuepic/vue-datepicker";
import TheTable from "@/components/TheTable.vue";
import {onMounted, ref} from "vue";
import '@vuepic/vue-datepicker/dist/main.css'

export default{
  data () {
    return{
      time_start:'2023-12-29',
      time_end:'2023-12-30',
      dataList: [],
    }
  },
  components:{
    VueDatePicker,
    TheTable,
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
      console.log(this.selectedTitles)
      this.back = 'waitting...'
      this.$axios.get('http://127.0.0.1:8000/api/participle?titles=' + this.selectedTitles)
          .then((response) => {
            const res = response.data
            console.log(res)
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
    };
  },
}
</script>

<style scoped>

</style>