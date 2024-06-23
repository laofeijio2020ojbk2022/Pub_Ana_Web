<template>
<el-container style="margin: 20px;">
  <el-header height="100px">
    <el-container style=
               "float: left;
                width: 30%;
                margin-left: 2%;
                margin-right: 1%;
                margin-top: 20px;
                border-radius: 5px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                background-color: #f5f5f5;">
      <VueDatePicker v-model="date" range format="yyyy-MM-dd" style="width: 100%; height: 100%"/>
    </el-container>

    <el-container style=
               "float: left;
                width: 30%;
                margin-left: 2%;
                margin-right: 1%;
                margin-top: 20px;
                border-radius: 5px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                background-color: #f5f5f5;">
      <el-select v-model="model" style="width: 100%;">
        <el-option value="all" label="活跃指数统计"></el-option>
        <el-option value="like" label="受欢迎度统计"></el-option>
        <el-option value="weight" label="用户权重统计"></el-option>
        <!-- 其他选项 -->
      </el-select>
    </el-container>

    <el-container style=
                 "float: left;
                  width: 30%;
                  margin-left: 2%;
                  margin-right: 1%;
                  margin-top: 20px;
                  border-radius: 5px;
                  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                  background-color: #f5f5f5;">
      <el-button @click="get_data" style="width: 100%; height: 37px">查询</el-button>
    </el-container>
  </el-header>

  <el-container style="height: 500px; margin-bottom: 30px">
      <el-main style=
                   "float: left;
                   width: 60%;
                   --el-main-padding: 0px;
                   margin-left: 3%;
                   border-radius: 10px;
                   box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                   background-color: #f5f5f5;">
        <TheMap :mapData=bloggerData.province></TheMap>
      </el-main>
      <el-main id="bar" style=
                   "--el-main-padding: 0px;
                   float: left;
                   width: 30%;
                   margin-left: 4%;
                   margin-right: 3%;
                   border-radius: 10px;
                   box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                   background-color: #f5f5f5;">
        <TheHorizontalBar :mapData=bloggerData.province></TheHorizontalBar>
      </el-main>
  </el-container>
  <el-container style=
                    "height: 300px;
                    margin: 10px 3% 40px;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                    background-color: #f5f5f5;">
    <el-main style="float: left; width: 30%; --el-main-padding: 0px;">
      <ThePie :data=bloggerData.birth></ThePie>
    </el-main>
    <el-main style="float: left; width: 30%; --el-main-padding: 0px;">
      <TheSpecialBar :data=bloggerData.birth_gender></TheSpecialBar>
    </el-main>
    <el-main style="float: left; width: 30%; --el-main-padding: 0px;">
      <ThePie :data=bloggerData.gender></ThePie>
    </el-main>
  </el-container>
  <el-container style="height: 450px; margin-bottom: 40px;">
    <el-main style="float: left; width: 20%;"></el-main>
    <el-main style=
                 "float: left;
                  width: 60%;
                  border-radius: 10px;
                  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                  background-color: #f5f5f5;">
      <img src="../../../../wordcloud.png" style="width: 100%; height: 97%;">
    </el-main>
    <el-main style="float: left; width: 20%;"></el-main>
  </el-container>
  <el-container height="200px" style="
             margin-bottom: 30px;
             margin-right: 3%;
             margin-left: 3%;
             border-radius: 10px;
             box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
             background-color: #f5f5f5;">
    <TheLine :timeData=bloggerData.create></TheLine>
  </el-container>
</el-container>
</template>

<script>
import TheMap from '@/components/TheMap.vue'
import TheHorizontalBar from '@/components/TheHorizontalBar.vue'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { ref, onMounted } from 'vue';
import ThePie from '@/components/ThePie.vue'
import TheSpecialBar from '@/components/TheSpecialBar.vue'
import TheLine from '@/components/TheLine.vue'

export default {
  components: {
    TheHorizontalBar,
    TheMap,
    VueDatePicker,
    ThePie,
    TheSpecialBar,
    TheLine,
  },
  data () {
    return{
      model:'all',
      time_start:'2023-12-29',
      time_end:'2023-12-30',
      mapData:[],
      bloggerData:{
        birth:[],
        birth_gender:[],
        create:[],
        gender:[],
        province:[],
        constellation:[],
      },
    }
  },
  methods: {
    async get_data() {
      this.back = 'waitting...'
      this.time_start = this.change_date(this.date[0])
      this.time_end = this.change_date(this.date[1])
      this.$axios.get('http://127.0.0.1:8000/api/blogger?model='
          + this.model + '&time_start=' + this.time_start + '&time_end=' + this.time_end)
          .then((response) => {
            const res = response.data
            console.log(res)
            this.bloggerData = res
            // console.log(this.time_start)
            // console.log(this.time_end)
          })
    },
    change_date(date) {
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Adding leading zero if necessary
      const day = date.getDate().toString().padStart(2, '0'); // Adding leading zero if necessary
      return `${year}-${month}-${day}`;
    }
  },
  setup() {
    const date = ref();

    // For demo purposes assign range from the current date
    onMounted(() => {
      const startDate = new Date();
      const endDate = new Date(new Date().setDate(startDate.getDate()));

      date.value = [startDate, endDate];
    });

    return {
      date,
    };
  },
}
</script>

<style scoped>

</style>