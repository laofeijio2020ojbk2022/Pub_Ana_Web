<template>
<el-container style="margin: 30px;">

  <el-space :size="80" style="margin-left: 30px">

    <el-space direction="vertical" :size="30">

      <el-card>
        <template #header>
          <p style="text-align: center; margin: 0px">匹配相同类型的微博用户头像</p>
        </template>
        <img src="../../../../img/gnn_dataset/img_300/big_img.jpg" alt="">
      </el-card>

      <el-space :size="50">

        <el-card @mouseover="handleMouseOver"
                 @mouseleave="handleMouseLeave"
                 @click="upload_img"
                 type="file"
                 ref="fileInput"
                 style="position: relative; cursor: pointer">
          <el-main
            v-show="show_upload"
            style="
              position: absolute;
              left: 50%;
              top: 50%;
              transform: translate(-50%, -50%);
              background-color: rgba(128, 128, 128, 0.9);
              border-radius: 5px;
              width: 100%;
              height: 100%;
              font-size: large;
              text-align: center;
              color: white;
            "
          >
            上传图片
          </el-main>
          <img v-show="!show_old" src="@/assets/img/疑惑.png" style="width: 50px; height: 50px">
          <img v-show="show_old" src="../../../../img/backend/upload_img/img.jpg" alt="" style="width: 50px; height: 50px">
        </el-card>

        <el-button size="large" @click="generate_img">
<!--          <el-icon><ArrowRightBold /></el-icon>-->
          <div style="margin-right: 10px; margin-left: 10px">点击开始匹配头像</div>
          <el-icon><ArrowRightBold /></el-icon>
        </el-button>

        <el-card @mouseover="handleMouseOver2(0)"
                 @mouseleave="handleMouseLeave2(0)"
                 @click="download_img(1)"
                 style="position: relative; cursor: pointer">
          <el-main
            v-show="show_download[0]"
            style="
              position: absolute;
              left: 50%;
              top: 50%;
              transform: translate(-50%, -50%);
              background-color: rgba(128, 128, 128, 0.9);
              border-radius: 5px;
              width: 100%;
              height: 100%;
              font-size: large;
              text-align: center;
              color: white;
            "
          >
            下载图片
          </el-main>
          <img v-show="!show_new" src="@/assets/img/疑惑.png" style="width: 50px; height: 50px">
          <img v-show="show_new" src="@/assets/img/output_img/1.jpg" alt="" style="width: 50px; height: 50px">
        </el-card>

      </el-space>

    </el-space>

    <el-space wrap style="width: 300px">
      <el-card
        @mouseover="handleMouseOver2(1)"
        @mouseleave="handleMouseLeave2(1)"
        @click="download_img(1)"
        style="position: relative; cursor: pointer">
        <el-main
          v-show="show_download[1]"
          style="
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(128, 128, 128, 0.9);
            border-radius: 5px;
            width: 100%;
            height: 100%;
            font-size: large;
            text-align: center;
            color: white;
          "
        >
          下载图片
        </el-main>
        <img v-show="!show_new" src="@/assets/img/疑惑.png" style="width: 50px; height: 50px">
        <img v-show="show_new" src="@/assets/img/output_img/1.jpg" alt="" style="width: 50px; height: 50px">
      </el-card>

      <el-card
        @mouseover="handleMouseOver2(2)"
        @mouseleave="handleMouseLeave2(2)"
        @click="download_img(2)"
        style="position: relative; cursor: pointer">
        <el-main
          v-show="show_download[2]"
          style="
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(128, 128, 128, 0.9);
            border-radius: 5px;
            width: 100%;
            height: 100%;
            font-size: large;
            text-align: center;
            color: white;
          "
        >
          下载图片
        </el-main>
        <img v-show="!show_new" src="@/assets/img/疑惑.png" style="width: 50px; height: 50px">
        <img v-show="show_new" src="@/assets/img/output_img/2.jpg" alt="" style="width: 50px; height: 50px">
      </el-card>

      <el-card
        @mouseover="handleMouseOver2(3)"
        @mouseleave="handleMouseLeave2(3)"
        @click="download_img(3)"
        style="position: relative; cursor: pointer">
        <el-main
          v-show="show_download[3]"
          style="
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(128, 128, 128, 0.9);
            border-radius: 5px;
            width: 100%;
            height: 100%;
            font-size: large;
            text-align: center;
            color: white;
          "
        >
          下载图片
        </el-main>
        <img v-show="!show_new" src="@/assets/img/疑惑.png" style="width: 50px; height: 50px">
        <img v-show="show_new" src="@/assets/img/output_img/3.jpg" alt="" style="width: 50px; height: 50px">
      </el-card>

      <el-card
        @mouseover="handleMouseOver2(4)"
        @mouseleave="handleMouseLeave2(4)"
        @click="download_img(4)"
        style="position: relative; cursor: pointer">
        <el-main
          v-show="show_download[4]"
          style="
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(128, 128, 128, 0.9);
            border-radius: 5px;
            width: 100%;
            height: 100%;
            font-size: large;
            text-align: center;
            color: white;
          "
        >
          下载图片
        </el-main>
        <img v-show="!show_new" src="@/assets/img/疑惑.png" style="width: 50px; height: 50px">
        <img v-show="show_new" src="@/assets/img/output_img/4.jpg" alt="" style="width: 50px; height: 50px">
      </el-card>

      <el-card
        @mouseover="handleMouseOver2(5)"
        @mouseleave="handleMouseLeave2(5)"
        @click="download_img(5)"
        style="position: relative; cursor: pointer">
        <el-main
          v-show="show_download[5]"
          style="
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(128, 128, 128, 0.9);
            border-radius: 5px;
            width: 100%;
            height: 100%;
            font-size: large;
            text-align: center;
            color: white;
          "
        >
          下载图片
        </el-main>
        <img v-show="!show_new" src="@/assets/img/疑惑.png" style="width: 50px; height: 50px">
        <img v-show="show_new" src="@/assets/img/output_img/5.jpg" alt="" style="width: 50px; height: 50px">
      </el-card>

      <el-card
        @mouseover="handleMouseOver2(6)"
        @mouseleave="handleMouseLeave2(6)"
        @click="download_img(6)"
        style="position: relative; cursor: pointer">
        <el-main
          v-show="show_download[6]"
          style="
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(128, 128, 128, 0.9);
            border-radius: 5px;
            width: 100%;
            height: 100%;
            font-size: large;
            text-align: center;
            color: white;
          "
        >
          下载图片
        </el-main>
        <img v-show="!show_new" src="@/assets/img/疑惑.png" style="width: 50px; height: 50px">
        <img v-show="show_new" src="@/assets/img/output_img/6.jpg" alt="" style="width: 50px; height: 50px">
      </el-card>

      <el-card
        @mouseover="handleMouseOver2(7)"
        @mouseleave="handleMouseLeave2(7)"
        @click="download_img(7)"
        style="position: relative; cursor: pointer">
        <el-main
          v-show="show_download[7]"
          style="
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(128, 128, 128, 0.9);
            border-radius: 5px;
            width: 100%;
            height: 100%;
            font-size: large;
            text-align: center;
            color: white;
          "
        >
          下载图片
        </el-main>
        <img v-show="!show_new" src="@/assets/img/疑惑.png" style="width: 50px; height: 50px">
        <img v-show="show_new" src="@/assets/img/output_img/7.jpg" alt="" style="width: 50px; height: 50px">
      </el-card>

      <el-card
        @mouseover="handleMouseOver2(8)"
        @mouseleave="handleMouseLeave2(8)"
        @click="download_img(8)"
        style="position: relative; cursor: pointer">
        <el-main
          v-show="show_download[8]"
          style="
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(128, 128, 128, 0.9);
            border-radius: 5px;
            width: 100%;
            height: 100%;
            font-size: large;
            text-align: center;
            color: white;
          "
        >
          下载图片
        </el-main>
        <img v-show="!show_new" src="@/assets/img/疑惑.png" style="width: 50px; height: 50px">
        <img v-show="show_new" src="@/assets/img/output_img/8.jpg" alt="" style="width: 50px; height: 50px">
      </el-card>

      <el-card
        @mouseover="handleMouseOver2(9)"
        @mouseleave="handleMouseLeave2(9)"
        @click="download_img(9)"
        style="position: relative; cursor: pointer">
        <el-main
          v-show="show_download[9]"
          style="
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(128, 128, 128, 0.9);
            border-radius: 5px;
            width: 100%;
            height: 100%;
            font-size: large;
            text-align: center;
            color: white;
          "
        >
          下载图片
        </el-main>
        <img v-show="!show_new" src="@/assets/img/疑惑.png" style="width: 50px; height: 50px">
        <img v-show="show_new" src="@/assets/img/output_img/9.jpg" alt="" style="width: 50px; height: 50px">
      </el-card>
    </el-space>

  </el-space>

  <el-button v-show="show_get_machine_img" @click="get_machine_img">ok</el-button>
</el-container>
</template>

<script>
import { ArrowRightBold } from '@element-plus/icons-vue'

export default {
  components: {
    ArrowRightBold
  },
  data () {
    return {
      show_get_machine_img: false,
      show_old: false,
      show_new: false,
      show_upload: false,
      show_download: [
          false,false,false,false,false,false,false,false,false,false,
      ],
      imageWidth: 300,
      imageHeight: 300,
      zoomStep: 10, // 调整大小的步长
    }
  },
  methods: {
    download_img(index) {
      console.log('ok')
      this.$axios.get('http://127.0.0.1:8000/api3/downloadImg',{
        params: {
          index: index,
        },
        responseType: 'arraybuffer',
      }).then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'image.jpg');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      })
      .catch(error => {
        console.error('图片下载失败', error);
      });
    },
    generate_img() {
      // console.log('ok')
      this.$axios.get('http://127.0.0.1:8000/api3/generateImg')
      // this.$axios.get('http://127.0.0.1:8000/api3/getMachineImg')
          .then((response) => {
            const res = response.data
            console.log(res)
          })
      setTimeout(() => {
            this.show_new = true;
          }, 2000); // 1000毫秒，即1秒
      },
    upload_img() {
      // console.log('ok')
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*'; // 可选：限制类型为图片文件
      input.onchange = (event) => {
        const file = event.target.files[0]; // 获取选择的文件
        this.uploadFile(file); // 调用上传文件的方法
      };
      input.click(); // 触发文件选择事件
    },
    uploadFile(file) {
      // console.log('ok2')
      const formData = new FormData();
      formData.append('file', file); // 将文件添加到FormData对象中
      this.$axios.post('http://127.0.0.1:8000/api3/uploadImg',formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
          }
        }).then((response) => {
            const res = response.data
            console.log(res)
          })
      this.show_old = true
    },
    handleMouseOver() {
      this.show_upload = true
    },
    handleMouseLeave() {
      this.show_upload = false
    },
    handleMouseOver2(i) {
      this.show_download[i] = true
    },
    handleMouseLeave2(i) {
      this.show_download[i] = false
    },
    get_machine_img(){
      this.$axios.get('http://127.0.0.1:8000/api3/getMachineImg', {
        params: {
          back: 'success'
        }
      }).then((response) => {
            const res = response.data
            console.log(res)
          })
    },
  }
}
</script>

<style scoped>

</style>