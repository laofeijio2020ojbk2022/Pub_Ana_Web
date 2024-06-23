<template>
<el-container>
  <el-header>
    <el-container style="margin-right: 10%; margin-left: 10%; margin-top: 30px">

      <el-main style="width: 45%">
        <el-button @click="get_cookies" style="width: 100%; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);">获取cookies</el-button>
      </el-main>

      <el-main style="width: 10%;"></el-main>

      <el-main style="width: 45%">
        <el-button @click="save_cookies" style="width: 100%; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);">存储cookies</el-button>
      </el-main>

    </el-container>
  </el-header>

  <el-container style="margin-top: 60px">

    <el-main style="width: 10%"></el-main>

    <el-main style=
                 "width: 80%;
                 box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
                 background-color: #8c939d;
                 border-radius: 5px;">
      <el-input v-model="cookie"
                type="textarea"
                autosize></el-input>
    </el-main>

    <el-main style="width: 10%"></el-main>

  </el-container>

</el-container>
</template>

<script>
import {ElMessage} from "element-plus";

export default {
  methods: {
    get_cookies(){
      this.$axios.get('http://127.0.0.1:8000/api2/getCookies',{
        params: {
          id: this.personaldata.id
        }
      }).then((response) => {
        const res = response.data
        // console.log(res)
        this.cookie = res.cookie
      })
    },
    save_cookies(){
      this.$axios.get('http://127.0.0.1:8000/api2/saveCookies',{
        params: {
          cookie:  this.cookie,
          id: this.personaldata.id
        }
      }).then((response) => {
        const res = response.data
        // console.log(res)
        if(res.back === 'success'){
            this.open1('保存成功')
          }else{
            this.open2('保存失败')
          }
      })
    }
  },
  data() {
    return{
      cookie: '',
      id: '',
    }
  },
  props: {
    personaldata:Object,
  },
  setup (){
    const open1 = (message) => {
        ElMessage({
          showClose: true,
          message: message,
          type: 'success',
      })
    }
    const open2 = (message) => {
        ElMessage({
          showClose: true,
          message: message,
          type: 'error',
      })
    }
    return {
      open1,
      open2,
    };
  },
}
</script>

<style scoped>

</style>