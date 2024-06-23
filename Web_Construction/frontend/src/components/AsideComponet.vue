<template>
  <el-aside
      width="200px"
      style="background-color: #27374D;">
    <el-menu
        :default-openeds="['1']"
        background-color="#27374D"
        text-color="white"
        :unique-opened="true">

      <el-sub-menu index="1">
        <template #title>
          <el-icon><User /></el-icon>用户画像
        </template>
        <router-link to="/active-user" >
          <el-menu-item index="1-1">活跃用户分析</el-menu-item>
        </router-link>
        <router-link to="/active-blogger">
          <el-menu-item index="1-2">活跃博主分析</el-menu-item>
        </router-link>
        <router-link to="/protrait">
          <el-menu-item index="1-3">匹配用户头像</el-menu-item>
        </router-link>
      </el-sub-menu>

      <el-sub-menu index="2">
        <template #title>
          <el-icon><ChatDotRound /></el-icon>热搜分析
        </template>
        <router-link to="/emotion">
          <el-menu-item index="2-1">热搜情感分析</el-menu-item>
        </router-link>
        <router-link to="/participle">
          <el-menu-item index="2-2">热搜热词分析</el-menu-item>
        </router-link>
      </el-sub-menu>

      <el-sub-menu index="3" v-if="admin >= 0">
        <template #title>
          <el-icon><Setting /></el-icon>用户管理
        </template>
        <router-link to="/personal">
          <el-menu-item index="3-1">个人信息管理</el-menu-item>
        </router-link>
        <router-link to="/admin">
          <el-menu-item index="3-2" v-if="admin === 1">用户信息管理</el-menu-item>
        </router-link>
      </el-sub-menu>

      <el-sub-menu index="4" v-if="admin === 1">
        <template #title>
          <el-icon><Refresh /></el-icon>实时爬虫
        </template>
        <router-link to="/cookies">
          <el-menu-item index="4-1">获取登录信息</el-menu-item>
        </router-link>
        <router-link to="/crawler">
          <el-menu-item index="4-2">获取微博数据</el-menu-item>
        </router-link><router-link to="/save">
          <el-menu-item index="4-3">实时数据合并</el-menu-item>
        </router-link>
      </el-sub-menu>

    </el-menu>
  </el-aside>
</template>

<style>
a{
  text-decoration: none;
}
.el-menu-item{
  background-color: #526D82;
}
</style>

<script>
import {ChatDotRound, Refresh, Setting, User} from "@element-plus/icons-vue";

export default {
  name: 'AsideComponet',
  components: {Refresh, User, ChatDotRound, Setting},
  props: {
    admin: {
      type: Number,
      required: true
    }
  }
}
</script>