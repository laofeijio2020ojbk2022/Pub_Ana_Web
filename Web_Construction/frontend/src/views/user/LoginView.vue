<template>
  <div class="gif-background">
    <el-container style="margin-bottom: 255px">
    <el-main style="width: 20%"></el-main>

<!--    窗口-->
    <el-main style="
    box-shadow: 0px 20px 80px 0px rgba(0,0,0,0.3);
    width: 60%;
    --el-main-padding: 0px;
    margin-top: 100px;">
      <el-container>
        <el-main style="width: 50%; --el-main-padding: 0px; background-color: #72767b; opacity: 0.9">
          <img src="../../assets/img/微博logal.png" style="width: 200px; margin: 23%">
        </el-main>

        <el-main style="width: 50%; --el-main-padding: 7%;">

          <el-container style="display: inline">
            <h2 style="margin: 0px; float: left">登录</h2>
            <div style="float: right; margin-top: 10px">
              <span>没有帐号？</span>
              <a @click="change_page">点此注册</a>
            </div>
          </el-container>

          <el-input placeholder="用户名" clearable v-model="username"></el-input>
          <div style="color: #d95c5c;" v-if="nameflag">用户名为必填项</div>

          <el-input placeholder="密码" show-password v-model="password" type="password" ></el-input>
          <div style="color: #d95c5c" v-if="passflag">密码为必填项</div>

          <el-button @click="get_register" style="width: 100%; background-color: #fe7300; color: white">立即登录</el-button>
          <div style="color: #d95c5c" v-if="hintflag">{{ hint }}</div>

          <a style="float: right; margin-top: 20px" href="">返回</a>

        </el-main>
      </el-container>
    </el-main>

    <el-main style="width: 20%"></el-main>
  </el-container>
  </div>
</template>

<script>
import { ElNotification } from 'element-plus';

export default {
  data () {
    return{
      username:'',
      nameflag:false,
      password:'',
      passflag:false,
      hint:'',
      hintflag:false,
    }
  },
  props: ['res'],
  methods:{
    get_register(){
      if (this.username == ''){
        this.nameflag = true
      }else {
        this.nameflag = false
      }
      if (this.password == ''){
        this.passflag = true
      }else {
        this.passflag = false
      }
      if (this.nameflag == false && this.passflag == false){
        const data = {
          name: this.username,
          pass: this.password
        }
        console.log(data)
        this.$axios.post('http://127.0.0.1:8000/api/login',data)
            .then((response) => {
              const res = response.data
              // console.log(res)
              if (res.back == 'success'){
                this.hintflag = false
                // console.log("登录成功")
                this.$emit('loginSuccess')
                this.open1(this.username)
                this.$emit('updateAdmin', res.data.admin)
                this.$emit('updateData', res.data)
              }else if(res.back == 'wrong pass'){
                this.hint = '密码错误'
                this.hintflag = true
                // console.log('密码错误')
              }else {
                this.hint = '没有该用户'
                this.hintflag = true
                // console.log('没有该用户')
              }
            })
      }
    },
    change_page(){
      // console.log('点击2')
      this.$emit('changePage', true);  // 当"a"标签在子组件中被点击时触发changePage事件，传递false给父组件
    }
  },
  setup() {
    const open1 = (message) => {
      ElNotification.success({
        title: '登录成功',
        message: '欢迎回来，亲爱的' + message + '先生',
        offset: 100,
      });
    };

    return {
      open1,
    };
  },
}
</script>

<style scoped>
.gif-background {
  //background-color: #000c17;
  background-image: url("../../assets/img/波浪.gif");
  top: 0;
  left: 0;
  width: 100%;
  background-size: contain;
}
a{
  color: #005980;
}
a:hover{
  color:#009fda;
  cursor: pointer;
}
.el-input{
  margin-top: 20px;
  height: 40px;
}
.el-button{
  margin-top: 20px;
  height: 40px;
}
</style>