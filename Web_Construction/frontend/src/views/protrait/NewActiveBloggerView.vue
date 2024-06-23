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

  <el-space :size="30" style="margin-left: 4%;">
      <el-card style="width: 610px; height: 600px">
        <template #header>
          <p style="text-align: center; margin: 0px">各省份热度指数地图</p>
        </template>
        <TheMap :mapData=mapData :map2Data=map2Data @send-data="handleReceivedData" @send-data-province="changeProvinceData"></TheMap>
      </el-card>
      <el-card style="width: 300px; height: 600px">
        <template #header>
          <p style="text-align: center; margin: 0px">热度指数排行</p>
        </template>
        <el-scrollbar style="height: 550px">
        <TheHorizontalBar :mapData=mapData :map2Data=map2Data :dataModel=dataModel></TheHorizontalBar>
        </el-scrollbar>
      </el-card>
  </el-space>

  <el-space v-show="timeData2.time[0] !== timeData2.time[1]" style="margin-left: 4%; margin-top: 30px">
    <el-card style="width: 940px;">
      <template #header>
        <p style="text-align: center; margin: 0px">每日热度指数时序图</p>
      </template>

      <div style="width: 100%"><TheLine :timeData="timeData2.date" @send-data-date="changeDateData"></TheLine></div>
    </el-card>
  </el-space>

  <el-space v-show="false" style="margin-left: 4%; margin-top: 30px;">
    <el-card style="width: 940px;">
      <template #header>
        <p style="text-align: center; margin: 0px">男女活跃度对比</p>
      </template>
      <div style="float: left; width: 10%;"><el-icon style="font-size: 40px; color: #409EFF; margin: 25px"><Male /></el-icon></div>
      <div style="float: left; width: 80%;"><TheMaleFemaleBar :data="timeData2.date"></TheMaleFemaleBar></div>
      <div style="float: left; width: 10%;"><el-icon style="font-size: 40px; color: #F56C6C; margin: 25px"><Female /></el-icon></div>
    </el-card>
  </el-space>

  <el-space style="margin-left: 4%; margin-top: 30px;">
    <el-card style="width: 940px;">
      <template #header>
        <p style="text-align: center; margin: 0px">当日活跃博主的年龄分布</p>
      </template>
      <TheSpecialBar :data="timeData2.age"></TheSpecialBar>
    </el-card>
  </el-space>

  <el-space :size="18" style="margin-left: 4%; margin-top: 30px;">
    <el-card style="width: 700px;">
      <template #header>
        <p style="text-align: center; margin: 0px">{{ timeData2.province }}博主最感兴趣的话题（Top10）</p>
      </template>
      <THeEmptyPie @send-topic-data="changeTopicData" :data=timeData2.title style="height: 426px"></THeEmptyPie>
    </el-card>

    <el-space direction="vertical" :size="20">
      <el-card style="width: 220px;">
        <template #header>
          <p style="text-align: center; margin: 0px">选择话题</p>
        </template>
        <el-input placeholder="全部话题" v-model="chooseTopic" clearable></el-input>
      </el-card>

      <el-card style="width: 220px;">
        <template #header>
          <p style="text-align: center; margin: 0px">选择省份</p>
        </template>
        <el-input placeholder="全部省份" v-model="chooseProvince" clearable></el-input>
      </el-card>

      <el-card style="width: 220px;">
        <template #header>
          <p style="text-align: center; margin: 0px">选择时间</p>
        </template>
        <el-input :placeholder="show_date(date)" v-model="chooseDate" clearable></el-input>
      </el-card>

      <el-card style="width: 220px;">
        <el-button style="width: 100%; height: 100%" @click="get_data">确认查询</el-button>
      </el-card>
    </el-space>
  </el-space>

  <el-space :size="18" style="margin-left: 4%; margin-top: 30px;">
    <el-card style="width: 300px;">
      <template #header>
        <p style="text-align: center; margin: 0px">{{ timeData2.province }}男博主（Top10）</p>
      </template>
      <el-table :data="timeData2.sort.male" :show-header="false" height="350px">
        <el-table-column type="expand">
          <template #default="props">
            <p class="txt_p">id: {{ props.row.info.uid }}</p>
            <p class="txt_p">用户名: {{ props.row.info.auther }}</p>
            <p class="txt_p">文案: {{ props.row.info.txt }}</p>
            <p class="txt_p">转发: {{ props.row.info.transmit }}</p>
            <p class="txt_p">评论: {{ props.row.info.comment }}</p>
            <p class="txt_p">点赞: {{ props.row.info.like }}</p>
            <p class="txt_p">热搜: {{ props.row.info.title }}</p>
            <p class="txt_p">生日: {{ props.row.info.birthday }}</p>
            <p class="txt_p">星座: {{ props.row.info.constellation }}</p>
            <p class="txt_p">账号创建时间: {{ props.row.info.createed_at }}</p>
            <p class="txt_p">地址: {{ props.row.info.location }}</p>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="" align="center"></el-table-column>
        <el-table-column prop="value" label="" align="center"></el-table-column>
      </el-table>
    </el-card>

    <el-card style="width: 300px;">
      <template #header>
        <p style="text-align: center; margin: 0px;">{{ timeData2.province }}活跃博主（Top10）</p>
      </template>
      <el-table :data="timeData2.sort.all" :show-header="false" height="350px">
        <el-table-column type="expand">
          <template #default="props">
            <p class="txt_p">id: {{ props.row.info.uid }}</p>
            <p class="txt_p">用户名: {{ props.row.info.auther }}</p>
            <p class="txt_p">文案: {{ props.row.info.txt }}</p>
            <p class="txt_p">转发: {{ props.row.info.transmit }}</p>
            <p class="txt_p">评论: {{ props.row.info.comment }}</p>
            <p class="txt_p">点赞: {{ props.row.info.like }}</p>
            <p class="txt_p">热搜: {{ props.row.info.title }}</p>
            <p class="txt_p">生日: {{ props.row.info.birthday }}</p>
            <p class="txt_p">星座: {{ props.row.info.constellation }}</p>
            <p class="txt_p">账号创建时间: {{ props.row.info.createed_at }}</p>
            <p class="txt_p">地址: {{ props.row.info.location }}</p>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="" align="center"></el-table-column>
        <el-table-column prop="value" label="" align="center"></el-table-column>
      </el-table>
    </el-card>

    <el-card style="width: 300px;">
      <template #header>
        <p style="text-align: center; margin: 0px">{{ timeData2.province }}女博主（Top10）</p>
      </template>
      <el-table :data="timeData2.sort.female" :show-header="false" height="350px">
        <el-table-column type="expand">
          <template #default="props">
            <p class="txt_p">id: {{ props.row.info.uid }}</p>
            <p class="txt_p">用户名: {{ props.row.info.auther }}</p>
            <p class="txt_p">文案: {{ props.row.info.txt }}</p>
            <p class="txt_p">转发: {{ props.row.info.transmit }}</p>
            <p class="txt_p">评论: {{ props.row.info.comment }}</p>
            <p class="txt_p">点赞: {{ props.row.info.like }}</p>
            <p class="txt_p">热搜: {{ props.row.info.title }}</p>
            <p class="txt_p">生日: {{ props.row.info.birthday }}</p>
            <p class="txt_p">星座: {{ props.row.info.constellation }}</p>
            <p class="txt_p">账号创建时间: {{ props.row.info.createed_at }}</p>
            <p class="txt_p">地址: {{ props.row.info.location }}</p>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="" align="center"></el-table-column>
        <el-table-column prop="value" label="" align="center"></el-table-column>
      </el-table>
    </el-card>
  </el-space>

</el-container>
</template>

<script>
import TheMap from '@/components/TheMap.vue'
import TheHorizontalBar from '@/components/TheHorizontalBar.vue'
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import { ref, onBeforeMount } from 'vue';
import TheLine from '@/components/TheLine.vue'
import THeEmptyPie from '@/components/TheEmptyPie.vue'
import TheMaleFemaleBar from '@/components/TheMaleFemaleBar.vue'
import {Female, Male} from "@element-plus/icons-vue";
import TheSpecialBar from '@/components/TheSpecialBar.vue'

export default {
  components: {
    Male,
    Female,
    VueDatePicker,
    TheMap,
    TheHorizontalBar,
    TheLine,
    THeEmptyPie,
    TheMaleFemaleBar,
    TheSpecialBar,
  },
  data () {
    return{
      model: 'all',
      mapData: [],
      map2Data: {
        male: [],
        female: [],
      },
      timeData2: {
        map: {
          all: [],
          male: [],
          female: [],
        },
        date: {
          male: [],
          female: [],
        },
        title: {
          all: [],
          male: [],
          female: [],
        },
        sort: {
          all: [],
          male: [],
          female: [],
        },
        age: {
          male: [],
          female: [],
        },
        time: [1, 1],
        province: '',
      },
      timeData: {
        male: [],
        female: [],
        sort: {
          all: [],
          male: [],
          female: [],
        },
        topic: {
          all: [],
          male: [],
          female: [],
        },
        province: '',
        title: '',
        time: [1, 1],
      },
      dataModel: 1,
      chooseTopic: '',
      chooseProvince: '',
      chooseDate: '',
    }
  },
  methods: {
    async get_data() {
      this.back = 'waitting...'
      if (this.chooseDate === ''){
        this.time_start = this.change_date(this.date[0])
        this.time_end = this.change_date(this.date[1])
      } else {
        this.time_start = this.chooseDate
        this.time_end = this.chooseDate
      }
      this.$axios.get('http://127.0.0.1:8000/api/blogger', {
        params: {
          model: this.model,
          time_start: this.time_start,
          time_end: this.time_end,
          topic: this.chooseTopic,
          province: this.chooseProvince
        }
      }).then((response) => {
        const res = response.data
        console.log(res)
        this.mapData = res.map.all
        this.map2Data = {
          male: res.map.male,
          female: res.map.female,
        }
        this.timeData2 = res
      })
    },
    change_date(date) {
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Adding leading zero if necessary
      const day = date.getDate().toString().padStart(2, '0'); // Adding leading zero if necessary
      return `${year}-${month}-${day}`;
    },
    show_date(date) {
      return this.change_date(date[0]) + ' - ' + this.change_date(date[1])
    },
    changeDateData(data) {
      this.chooseDate = data
    },
    changeProvinceData(data) {
      this.chooseProvince = data
    },
    changeTopicData(data) {
      this.chooseTopic = data
    },
    handleReceivedData(data) {
      this.dataModel = data
    },
  },
  setup() {
    const date = ref();
    const time_start = ref('');
    const time_end = ref('');

    // For demo purposes assign range from the current date
    onBeforeMount(() => {
      const startDate = new Date();
      const endDate = new Date(new Date().setDate(startDate.getDate()));

      date.value = [startDate, endDate];
      console.log(date.value)
    });

    return {
      date,
      time_start,
      time_end,
    };
  },
}
</script>

<style scoped>
.txt_p{
  padding-left: 30px;
  margin-bottom: 2px;
}
</style>
