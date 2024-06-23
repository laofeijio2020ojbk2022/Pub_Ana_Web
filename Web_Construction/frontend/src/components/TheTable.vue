<template>
  <el-table
    ref="multipleTableRef"
    :data="filterTableData"
    style="width: 100%; height: 100%"
    @selection-change="handleSelectionChange"
  >
    <el-table-column type="selection" width="50"/>
    <el-table-column prop="title" label="标题"/>
    <el-table-column prop="label" label="标签" width="140"/>
    <el-table-column prop="time" label="上榜时间" sortable width="140"/>
    <el-table-column prop="hot" label="热点" sortable width="140"/>

    <el-table-column width="140">
      <template #header>
        <el-input :prefix-icon="Search" v-model="search" size="small" placeholder="检索热搜"/>
      </template>
    </el-table-column>

  </el-table>
</template>

<script>
import { ref, watch, onMounted, computed } from 'vue';
// import { ElTable } from 'element-plus';
import { Search } from '@element-plus/icons-vue'

export default {
  name:'TheTable',
  computed: {
    Search() {
      return Search
    }
  },
  props:{
    data:{
      type:Array,
      required:true,
    }
  },
  setup(props, { emit }) {
    const multipleTableRef = ref(null);
    const tableData = ref([]);

    const selectedTitles = ref([]); // 用于存储选中数据的title信息

    const handleSelectionChange = (selection) => {
      selectedTitles.value = selection.map((item) => item.title); // 在选中项发生改变时，更新selectedTitles

      // console.log('选中')
      // console.log(selectedTitles.value.join(', '))
      // 向父组件发送选中的title数据
      emit('selected-titles', selectedTitles.value.join(', '));
    };

    // 监听父组件传递的数据变化
    watch(
      () => props.data,
      (newVal) => {
        tableData.value = newVal;
      }
    );

    // 组件挂载后执行的操作
    onMounted(() => {
      tableData.value = props.data
      // 这里可以执行一些初始化操作
    });

    const search = ref('')
    const filterTableData = computed(() =>
      tableData.value.filter(
        (data) =>
          !search.value ||
          data.title.toLowerCase().includes(search.value.toLowerCase())
      )
    )

    return {
      multipleTableRef,
      tableData,
      handleSelectionChange,
      filterTableData,
      search,
    };
  },
};
</script>
