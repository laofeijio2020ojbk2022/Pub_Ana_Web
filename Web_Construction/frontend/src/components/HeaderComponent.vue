<template>
<el-container style="display: inline">
  <el-container style="float: right;">

    <el-container style="margin: 10px; background-size: 50px">
      <router-link to="/">
        <div style=
                 "width: 50px;
                 border-radius: 25px;
                 border: #72767b;
                 background-color: #9DB2BF">
          <el-icon size="30px" style="margin: 10px"><HomeFilled /></el-icon>
        </div>
      </router-link>
    </el-container>

    <el-container style="margin: 10px">
      <img src="../assets/img/images.png" width=50px style="border-radius: 25px" @click="login">
    </el-container>
<!--    <el-container style="margin: 10px">-->
<!--      <img src="@/assets/跳舞猫猫.gif" width=50px style="border-radius: 25px">-->
<!--    </el-container>-->
  </el-container>

  <el-container style="float: left;">
    <el-container style="width: 400px"></el-container>
    <h1 style="font-size: xxx-large; margin: 0px; color: #DDE6ED">微博数据分析平台</h1>
  </el-container>
</el-container>
</template>

<script>
import { HomeFilled } from '@element-plus/icons-vue'

export default {
  name: 'HeaderComponent',
  components: {
    HomeFilled,
  },
  methods:{
    login() {
      this.$emit('loginPage')
    }
  }
}
</script>

<style>
a {
  color: #ffffff;
}
</style>