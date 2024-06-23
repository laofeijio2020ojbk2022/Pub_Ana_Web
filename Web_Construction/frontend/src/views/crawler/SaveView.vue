<template>
<el-container>

  <el-space style="margin: 60px" size="large" wrap>

    <el-card
      style="width: 300px; height: 400px"
      class="box-card"
      @mouseover="handleMouseOver"
      @mouseleave="handleMouseLeave"
      @click="save_title"
    >
      <div class="card-content">
        <h3>Part 1: 存储热搜</h3>
        <br><br>
        <el-container style="margin-left: 5px">
          <el-progress type="dashboard" :percentage="titleProgress">
            <template #default="{ percentage }">
              <span class="percentage-value">{{ percentage }}%</span>
              <span class="percentage-label">Progressing</span>
            </template>
          </el-progress>
        </el-container>
      </div>
    </el-card>

    <el-card
      style="width: 300px; height: 400px"
      class="box-card"
      @mouseover="handleMouseOver"
      @mouseleave="handleMouseLeave"
      @click="save_post"
    >
      <div class="card-content">
        <h3>Part 2: 存储热帖</h3>
        <br><br>
        <el-container style="margin-left: 5px">
          <el-progress type="dashboard" :percentage="postProgress">
            <template #default="{ percentage }">
              <span class="percentage-value">{{ percentage }}%</span>
              <span class="percentage-label">Progressing</span>
            </template>
          </el-progress>
        </el-container>
      </div>
    </el-card>

    <el-card
      style="width: 300px; height: 400px"
      class="box-card"
      @mouseover="handleMouseOver"
      @mouseleave="handleMouseLeave"
      @click="save_comment"
    >
      <div class="card-content">
        <h3>Part 3: 存储热评</h3>
        <br><br>
        <el-container style="margin-left: 5px">
          <el-progress type="dashboard" :percentage="commentProgress">
            <template #default="{ percentage }">
              <span class="percentage-value">{{ percentage }}%</span>
              <span class="percentage-label">Progressing</span>
            </template>
          </el-progress>
        </el-container>
      </div>
    </el-card>

  </el-space>



</el-container>
</template>

<script>

export default {
  data() {
    return{
      titleProgress: 0,
      postProgress: 0,
      commentProgress: 0,
      commentsocket: null,
    }
  },
  methods: {
    save_title() {
      this.$axios.get('http://127.0.0.1:8000/api2/saveTitle')
          .then((response) => {
            const res = response.data
            // console.log(res)
            if(res.back === 'success'){
              this.titleProgress = 100
            }
          })
    },
    save_post() {
      this.setupWebSocket('savePostProgress')
      this.$axios.get('http://127.0.0.1:8000/api2/savePost')
          .then((response) => {
            const res = response.data
            console.log(res)
            // if(res.back === 'success'){
            //   this.postProgress = 100
            // }
          })
    },
    save_comment() {
      this.setupWebSocket('saveCommentProgress')
      this.$axios.get('http://127.0.0.1:8000/api2/saveComment')
          .then((response) => {
            const res = response.data
            console.log(res)
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
      if(choose === 'saveCommentProgress'){
        ws.onmessage = (event) => {
          // console.log('ok')
          const message = JSON.parse(event.data).message;
          // console.log('收到的消息：', message)
          this.commentProgress = message.progress
          // if(message.flag){
          //   this.commentProgressStatus = 'success'
          // }
        }
      }else if(choose === 'savePostProgress'){
        ws.onmessage = (event) => {
          // console.log('ok')
          const message = JSON.parse(event.data).message;
          // console.log('收到的消息：', message)
          this.postProgress = message.progress
          // if(message.flag){
          //   this.commentProgressStatus = 'success'
          // }
        }
      }
      this.commentsocket = ws
    },
    handleMouseOver(event) {
      event.target.classList.add('hovered');
    },
    handleMouseLeave(event) {
      event.target.classList.remove('hovered');
    },
  },
}
</script>

<style scoped>
.box-card {
  transition: all 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  cursor: pointer;
}
.box-card.hovered {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  background-color: white;
}
.card-content {
  padding: 59px;
}

.percentage-value {
  display: block;
  margin-top: 10px;
  font-size: 28px;
}
.percentage-label {
  display: block;
  margin-top: 10px;
  font-size: 12px;
}
</style>