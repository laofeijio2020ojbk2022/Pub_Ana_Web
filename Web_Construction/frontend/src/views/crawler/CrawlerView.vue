<template>
<el-container>

  <el-header>
    <el-container style="margin-top: 30px">

      <el-main style="width: 30%"></el-main>

      <el-main style="width: 40%">
        <el-button @click="get_title" style="width: 100%">step1：获取热搜</el-button>
      </el-main>

      <el-main style="width: 30%"></el-main>

    </el-container>
  </el-header>

  <el-container style="height: 400px; margin-top: 70px;">

    <el-main style="width: 10%"></el-main>

    <el-main style=
                 "width: 80%;
                 background-color: white;
                 box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
                 border-radius: 5px;height: 100%;"
             id="bar">
      <el-table :data="data" style="width: 100%;height: 100%;">

        <el-table-column prop="title" label="标题" align="center"></el-table-column>
        <el-table-column prop="label" label="标签" align="center"></el-table-column>
        <el-table-column prop="hot" label="热度" align="center"></el-table-column>
        <el-table-column prop="time" label="时间" align="center"></el-table-column>

      </el-table>
    </el-main>

    <el-main style="width: 10%"></el-main>

  </el-container>

  <el-header>
    <el-container style="margin-top: 30px">

      <el-main style="width: 30%"></el-main>

      <el-main style="width: 40%">
        <el-button @click="get_post" style="width: 100%">step2：获取热帖</el-button>
      </el-main>

      <el-main style="width: 30%"></el-main>

    </el-container>
  </el-header>

  <el-container style="margin-top: 70px;">

    <el-main style="width: 5%"></el-main>

    <el-main style="width: 15%">
      <el-progress
          type="circle"
          :percentage="postProgress"
          :status="postProgressStatus"
          style="background-color: rgb(221, 230, 237); border-radius: 50%;box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);"></el-progress>
    </el-main>

    <el-main style="width: 70%; background-color: white; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); height: 200px;">
      <el-table fit="false" height="100%" :data="postdata" style="width: 100%" ref="postTable" @scroll="tableScroll">

        <el-table-column type="expand">
          <template #default="props">
            <p m="t-0 b-2">文案: </p>
            <p m="t-0 b-2">{{ props.row.txt2 }}</p>
          </template>
        </el-table-column>

        <el-table-column prop="mid" label="微博id" align="center"></el-table-column>
        <el-table-column prop="auther" label="作者" align="center"></el-table-column>
        <el-table-column prop="uid" label="作者id" align="center"></el-table-column>
        <el-table-column prop="title" label="热搜" align="center"></el-table-column>
        <el-table-column prop="transmit" label="转发" align="center"  width="60"></el-table-column>
        <el-table-column prop="comment" label="评论" align="center"  width="60"></el-table-column>
        <el-table-column prop="like" label="点赞" align="center" width="60"></el-table-column>

<!--        <el-table-column prop="txt2" label="文案" align="center"></el-table-column>-->


      </el-table>
    </el-main>

    <el-main style="width: 5%"></el-main>

  </el-container>

  <el-header>
    <el-container style="margin-top: 30px">

      <el-main style="width: 30%"></el-main>

      <el-main style="width: 40%">
        <el-button @click="get_detail" style="width: 100%">step3：获取热评</el-button>
      </el-main>

      <el-main style="width: 30%"></el-main>

    </el-container>
  </el-header>

  <el-container style="margin-top: 70px;">

    <el-main style="width: 5%"></el-main>

    <el-main style="width: 90%; border-radius: 5px; box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2); background-color: rgb(221, 230, 237);">
      <el-progress
          :percentage="detailProgress"
          stroke-width="15"
          :status="detailProgressStatus"
          striped
          striped-flow
          style=""></el-progress>
    </el-main>

    <el-main style="width: 5%"></el-main>

  </el-container>

  <el-container style="margin-bottom: 70px">
    <el-main  v-show="detaildata !== ''" style="text-align: center">正在爬取热搜评论中。。。 {{ this.detaildata }} 。。。</el-main>
  </el-container>


</el-container>
</template>

<script>
export default {
  methods: {
    get_title() {
      this.$axios.get('http://127.0.0.1:8000/api2/getTitle',{
        params: {
          id:this.personaldata.id
        }
      }).then((response) => {
          const res = response.data
          // console.log(res)
          this.data = res.data
        })
    },
    get_post() {
      this.postProgressStatus = ''
      this.setupWebSocket('postProgress')
      this.$axios.get('http://127.0.0.1:8000/api2/getPost', {
        params: {
          id:this.personaldata.id
        }
      }).then((response) => {
          const res = response.data
          console.log('getPostProgress:', res)
        })
    },
    get_detail() {
      this.detailProgressStatus = ''
      this.setupWebSocket('detailProgress')
      this.$axios.get('http://127.0.0.1:8000/api2/getDetail', {
        params: {
          id:this.personaldata.id
        }
      }).then((response) => {
          const res = response.data
          console.log('getDetailProgress', res)
        })
    },
    setupWebSocket(choose) {
      const ws = new WebSocket('ws://127.0.0.1:8000/ws/chat/' +choose+ '/');
      ws.onopen = () => {
        console.log('WebSocket连接已打开');
      }
      ws.onclose = (e) => {
          console.error('断开连接：', e)
        }
      if(choose === 'postProgress'){
        ws.onmessage = (event) => {
          const message = JSON.parse(event.data).message;
          console.log('收到的消息：', message)
          this.postProgress = message.progress
          // this.postdata = message.data
          for(let i = 0; i < message.data.length; i++) {
            this.postdata.push(message.data[i])
          }
          this.tableScroll()
          if(message.flag){
            this.postProgressStatus = 'success'
          }
          ws.send(JSON.stringify({'data': 'ok'}))
        }
        this.postsocket = ws
      }else if(choose === 'detailProgress'){
        ws.onmessage = (event) => {
          const message = JSON.parse(event.data).message;
          console.log('收到的消息：', message)
          this.detailProgress = message.progress
          this.detaildata = message.data
          // for(let i = 0; i < message.data.length; i++) {
          //   this.detaildata.push(message.data[i])
          // }
          // this.tableScroll()
          if(message.flag){
            this.detailProgressStatus = 'success'
            this.detaildata = ''
          }
        }
        this.detailsocket = ws
      }
    },
    tableScroll() {
      this.$nextTick(() => {
        if (this.$refs.postTable && this.$refs.postTable.$el) {
          const tableContentHeight = this.$refs.postTable.$el.querySelector("tbody").offsetHeight; // 获取表格内容的实际高度
          this.$refs.postTable.setScrollTop(tableContentHeight); // 将表格滚动到最底部行的实际位置
        }
      });
    },
  },
  props: {
    personaldata:Object,
  },
  data() {
    return{
      data: [],
      postsocket: null,
      postProgress: 0,
      postProgressStatus: '',
      postdata: [],

      detailsocket: null,
      detailProgress: 0,
      detailProgressStatus: '',
      detaildata: '',
    }
  },
  mounted() {
  }
}
</script>

<style scoped>
#bar::-webkit-scrollbar {
  width: 0px;  /* 设置滚动条宽度 */
}
#bar::-webkit-scrollbar-thumb {
  background-color: #ccc;  /* 设置滑块颜色 */
  border-radius: 5px;  /* 设置滑块圆角 */
}
#post .el-table__body-wrapper .cell {
  white-space: nowrap;      /* 不换行 */
  overflow: hidden;         /* 内容超出隐藏 */
  text-overflow: ellipsis;  /* 显示省略号 */
}
</style>