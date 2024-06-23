<template>
  <div class="common-layout">
<!--    <el-button @click="truu"></el-button>-->
    <el-container v-if="home_flag">
<!--      头-->
      <el-header height="70px" style="background-color: #27374D;">
        <HeaderComponent @loginPage="handleLoginSuccess"></HeaderComponent>
      </el-header>

      <el-container style="height: 530px">

        <!--      左侧导航栏-->
        <AsideComponet :admin="admin"></AsideComponet>

        <!--        右侧内容-->
        <el-container>
          <el-main id="theview" style="--el-main-padding:0px; background-color: #DDE6ED">
            <router-view :personaldata="personaldata"></router-view>
          </el-main>
<!--          <el-footer style="background-color: #D4CDCD"></el-footer>-->
        </el-container>

      </el-container>

    </el-container>

    <el-container v-if="!home_flag">
      <RegisterView v-if="register_flag" @changePage="updateRegisterFlag"></RegisterView>
      <LoginView v-if="!register_flag"
                 @changePage="updateRegisterFlag"
                 @loginSuccess="handleLoginSuccess"
                 @updateAdmin="handleUpdateAdmin"
                 @updateData="handleUpdateData"></LoginView>
    </el-container>
  </div>
</template>

<script>
import AsideComponet from '@/components/AsideComponet.vue'
import HeaderComponent from '@/components/HeaderComponent.vue'
import RegisterView from "@/views/user/RegisterView.vue"
import LoginView from '@/views/user/LoginView.vue'

export default {
  components: {
    LoginView,
    RegisterView,
    AsideComponet,
    HeaderComponent,
  },
  data () {
    return{
      home_flag: true,
      register_flag: false,
      admin: -1,
      personaldata: {}
    }
  },
  methods:{
    // truu() {
    //   this.home_flag = !this.home_flag
    // },
    updateRegisterFlag(flag) {
      this.register_flag = flag;  // 更新register_flag的值
    },
    handleLoginSuccess() {
      // console.log('变')
      this.home_flag = !this.home_flag
    },
    handleUpdateAdmin(value) {
      this.admin = value; // 将子组件传递的值更新到父组件的 admin 参数
    },
    handleUpdateData(value) {
      // console.log(value)
      this.personaldata = value
    }
  }
}
</script>


<style scoped>
#theview::-webkit-scrollbar{
  display: none;
}
</style>