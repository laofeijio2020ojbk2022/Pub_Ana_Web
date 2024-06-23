<template>

<!--  <div style="height: 100px; background-color: white">-->
<!--    <h3 style="font-size: xx-large; margin: 0px; text-align: center">-->
<!--      {{ personaldata.name }}的个人空间-->
<!--    </h3>-->
<!--  </div>-->

<div>

  <div style="overflow: auto;" class="gif-background">

    <div style="float: left; width: 25%">
      <img src="../../assets/img/images.png" style="width: 130px; border-radius: 65px; margin-left: 25%; margin-top: 25%">
      <h2 style="text-align: center; background-color: white; width: 40%; margin-left: 28%"> {{ personaldata.name }}</h2>

      <div style="margin-left: 14%">
        <el-button type="info" text bg v-if="change" @click="toggleEdit">
          修改<br/>用户<br/>信息</el-button>
        <el-button type="danger" text bg v-else @click="submintChange">
          确认<br/>提交<br/>修改</el-button>
      </div>
    </div>

    <div style="float: left; width: 50%; background-color: white">
      <el-container style="display: inline-table; margin-top: 30px; margin-bottom: 5px">

        <el-main class="row">
          <div class="left">id:</div>
          <div class="right">
            <el-input
                readonly="false"
                type="text"
                :placeholder="id"
            ></el-input>
          </div>
        </el-main>

        <el-main v-for="(value, key) in thelist" :key="key" class="row">
          <div class="left">{{ thelist[key] }}:</div>
          <div class="right">
            <el-input
                v-model="localData[key]"
                :readonly="!editing"
                :maxlength="getMaxleng(key)"
                show-word-limit
                :type="getFieldType(key)"
                :rows="4"
                :placeholder="getPlaceholder(key, localData[key])"
            ></el-input>
          </div>
        </el-main>

        <el-main class="row">
          <div class="left">管理员权限:</div>
          <div class="right">
            <el-input
                readonly="false"
                type="text"
                :placeholder="admin?'管理员':'普通用户'"
            ></el-input>
          </div>
        </el-main>

      </el-container>
    </div>

    <div style="float: left; width: 25%; background-color: #DDE6ED"></div>

  </div>

<!--  <div>-->
<!--    <img src="../../assets/img/波浪.gif" style="width: 100%; height: 100%; position: fixed; top: -2px; left: 50px; z-index: -1">-->
<!--  </div>-->

</div>
</template>

<script>
import { ElMessage  } from 'element-plus';

export default {
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
  props: {
    personaldata:Object,
  },
  data (){
    return{
      localData: {},
      editing: false,
      change: true,
      thelist: {
        name:'昵称',
        password:'密码',
        sex:'性别',
        birth:'生日',
        txt:'留言',
      },
      admin: this.personaldata.admin,
      id: this.personaldata.id,
    }
  },
  created() {
    // 将父组件传来的数据复制到本地数据中
    this.localData = { ...this.personaldata };
  },
  methods: {
    toggleEdit() {
      this.editing = !this.editing;
      this.change = !this.change;
    },
    submintChange() {
      this.$axios.post('http://127.0.0.1:8000/api/changeUser', this.localData)
          .then((response) => {
            const res = response.data
            // console.log(res)
            if(res.back === 'success'){
              this.open1('修改成功')
              this.editing = !this.editing;
              this.change = !this.change;
            }else{
              this.open2('修改失败')
            }
          })
    },
    getPlaceholder(key, value) {
      if(key === 'txt'){
        if(!value){
          return '该用户很懒，什么也没写'
        }
      }else if(key === 'sex'){
        return '0:女；1:男'
      }else if(key === 'birth'){
        return '2020-01-01'
      }
    },
    getFieldType(key) {
      if(key === 'txt'){
        return 'textarea'
      }else if(key === 'password'){
        return 'password'
      } else{
        return 'text'
      }
    },
    getMaxleng(key){
      if(key === 'name'){
        return 256
      }else if(key === 'sex'){
        return 1
      }else if(key === 'birth'){
        return 10
      }else if(key === 'txt')
        return 1024
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

#bar::-webkit-scrollbar {
  width: 0px;  /* 设置滚动条宽度 */
}
#bar::-webkit-scrollbar-thumb {
  background-color: #ccc;  /* 设置滑块颜色 */
  border-radius: 5px;  /* 设置滑块圆角 */
}

.row {
  display: flex;
  align-items: center;
  //margin-bottom: 10px;
}

.left {
  width: 100px;
  text-align: right;
  margin-right: 10px;
}

.right {
  flex: 1;
}

.el-input {
  width: 300px;
}

.el-button {
  width: 100px;
  height: 150px;
  margin-left: 40px;
  margin-top: 40px;
  font-size: x-large;
  line-height: 1.5;
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
}
</style>