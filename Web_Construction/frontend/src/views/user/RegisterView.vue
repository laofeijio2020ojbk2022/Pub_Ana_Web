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
        <el-main style="width: 50%; --el-main-padding: 7%;">

          <el-container style="display: inline">
            <h2 style="margin: 0px; float: left">注册</h2>
            <div style="float: right; margin-top: 10px">
              <span>已有帐号？</span>
              <a @click="change_page">点此登录</a>
            </div>
          </el-container>

          <el-input placeholder="用户名" clearable v-model="username"></el-input>
          <div style="color: #d95c5c;" v-if="nameflag">用户名为必填项</div>

          <el-input placeholder="密码" show-password v-model="password" type="password" ></el-input>
          <div style="color: #d95c5c" v-if="passflag">密码为必填项</div>

          <el-button @click="get_register" style="width: 100%; background-color: #fe7300; color: white">立即注册</el-button>
          <div style="color: #d95c5c" v-if="userflag">用户已存在</div>

          <a style="float: right; margin-top: 20px" href="">返回</a>

        </el-main>

        <el-main style="width: 50%; --el-main-padding: 0px; background-color: #72767b; opacity: 0.9">
          <img src="../../assets/img/微博logal.png" style="width: 200px; margin: 23%">
        </el-main>
      </el-container>
    </el-main>

    <el-main style="width: 20%"></el-main>
  </el-container>
  </div>
</template>

<script>
import { ElMessage  } from 'element-plus';

export default {
  setup (){
    const open1 = () => {
        ElMessage({
          showClose: true,
          message: '注册成功',
          type: 'success',
      })
    }
    return {
      open1,
    };
  },
  data () {
    return{
      username:'',
      nameflag:false,
      password:'',
      passflag:false,
      userflag:false,
    }
  },
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
        this.$axios.post('http://127.0.0.1:8000/api/register',data)
            .then((response) => {
              const res = response.data
              // console.log(res.back)
              if (res.back == 'failed'){
                this.userflag = true
              }else {
                this.open1()
                this.change_page()
              }
            })
      }
    },
    change_page(){
      // console.log('点击')
      this.$emit('changePage', false);  // 当"a"标签在子组件中被点击时触发changePage事件，传递false给父组件
    }
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