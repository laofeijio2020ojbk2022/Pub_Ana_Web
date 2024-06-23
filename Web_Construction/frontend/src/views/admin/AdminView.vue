<template>
<el-container class="gif-background">

  <el-header height="100px" style="background-color: white; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);">
    <el-container style="margin-top: 15px">
      <el-main style="with: 5%"></el-main>
      <el-main style="width: 5%">
        <h2 style="margin: 0px">用户id:</h2>
      </el-main>
      <el-main style="width: 40%">
        <el-input placeholder="默认查询所有用户" v-model="id" style="width: 100%;"></el-input>
      </el-main>
      <el-main style="with: 45%">
        <el-button @click="getUser" style="width: 100%">查询</el-button>
      </el-main>
      <el-main style="with: 5%"></el-main>
    </el-container>
  </el-header>

  <el-container style="margin-bottom: 50px; height: 400px; margin-top: 50px; width: 100%">

    <el-main style="width: 10%"></el-main>

    <el-main style=
                 "width: 80%;
                 background-color: white;
                 box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
                 border-radius: 5px;
                 height: 100%">
      <el-table :data="data" style="width: 100%; height: 100%">

        <el-table-column prop="u_id" label="用户id" align="center"></el-table-column>
        <el-table-column prop="u_name" label="用户姓名" align="center"></el-table-column>
        <el-table-column prop="u_password" label="用户密码" align="center"></el-table-column>
        <el-table-column prop="u_sex" label="用户性别" align="center"></el-table-column>
        <el-table-column prop="u_birth" label="用户生日" align="center" width="120"></el-table-column>
        <el-table-column prop="u_txt" label="用户留言" align="center"></el-table-column>
        <el-table-column prop="u_admin" label="用户权限" align="center"></el-table-column>

        <el-table-column label="操作" width="200" align="center">
          <template v-slot="scope">
            <el-button type="primary" size="mini" @click="handleModify(scope.row)">修改</el-button>
            <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>

      </el-table>
    </el-main>

    <el-main style="width: 10%"></el-main>

  </el-container>

  <el-dialog v-model="dialogFormVisible" title="输入你要修改的内容" width="500" style="text-align: center">

    <el-form>

      <div class="row">
        <div class="left">用户id:</div>
        <div class="right">
          <el-input
              readonly="false"
              type="text"
              :placeholder="user.u_id"
          ></el-input>
        </div>
      </div>

      <div v-for="(value, key) in thelist" :key="key" class="row">
        <div class="left">{{ thelist[key] }}:</div>
        <div class="right">
          <el-input
              v-model="user[key]"
              :maxlength="getMaxleng(key)"
              show-word-limit
              :type="getFieldType(key)"
              :placeholder="getPlaceholder(key, user[key])"
          ></el-input>
        </div>
      </div>

    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="changeUser">提交</el-button>
      </div>
    </template>
  </el-dialog>

</el-container>
</template>

<script>
import {ElMessage} from "element-plus";

export default {
  data() {
    return{
      data: [],
      id: '',
      dialogFormVisible: false,
      user: {},
      user2: {},
      thelist: {
        u_name:'昵称',
        u_password:'密码',
        u_sex:'性别',
        u_birth:'生日',
        u_txt:'留言',
        u_admin:'管理员权限',
      },
    }
  },
  methods: {
    changeUser(){
      this.user2 = {
        id: this.user.u_id,
        name: this.user.u_name,
        password: this.user.u_password,
        sex: this.user.u_sex,
        birth: this.user.u_birth,
        txt: this.user.u_txt,
        admin: this.user.u_admin,
      }
      // console.log(this.user2)
      this.$axios.post('http://127.0.0.1:8000/api/changeUser', this.user2)
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
      this.dialogFormVisible = false
    },
    getUser(){
      this.$axios.get('http://127.0.0.1:8000/api/getUser', {
        params: {
          id: this.id
        }
      }).then((response) => {
            const res = response.data
            // console.log(res)
            this.data = res.value
            // console.log(this.data)
          })
    },
    handleModify(row){
      this.dialogFormVisible = true
      console.log(row)
      this.user = row

    },
    handleDelete(row){
      // console.log(row.u_id)
      this.$axios.get('http://127.0.0.1:8000/api/deleteUser?u_id=' + row.u_id)
          .then((response) => {
            const res = response.data
            console.log(res)
          })
      this.getUser()
    },
    getMaxleng(key){
      if(key === 'u_name'){
        return 256
      }else if(key === 'u_sex' || key === 'u_admin'){
        return 1
      }else if(key === 'u_birth'){
        return 10
      }else if(key === 'u_txt')
        return 1024
    },
    getFieldType(key) {
      if(key === 'u_txt'){
        return 'textarea'
      }else{
        return 'text'
      }
    },
    getPlaceholder(key, value) {
      if(key === 'u_txt'){
        if(!value){
          return '该用户很懒，什么也没写'
        }
      }else if(key === 'u_sex'){
        return '0:女；1:男'
      }else if(key === 'u_birth'){
        return '2020-01-01'
      }else if(key === 'u_admin'){
        return  '0:普通用户；1:管理员'
      }
    },
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
.gif-background {
  //background-color: #000c17;
  background-image: url("../../assets/img/波浪.gif");
  top: 0;
  left: 0;
  width: 100%;
  background-size: contain;
}

.row {
  display: flex;
  align-items: center;
  margin-top: 20px;
}

.left {
  width: 80px;
  text-align: right;
  margin-right: 30px;
}

.right {
  flex: 1;
  margin-right: 20px;
}
</style>