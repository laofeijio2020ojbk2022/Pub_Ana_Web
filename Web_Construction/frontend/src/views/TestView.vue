<script>
import TodoItem from "@/components/todoItem.vue";

export default {
  components: {
    todoItem: TodoItem,
  },
  data () {
    return {
      text: '',
      back: '空',
      newTodoText: '',
      todos: [
        {
          id: 1,
          title: 'Do the dishes'
        },
        {
          id: 2,
          title: 'Take out the trash'
        },
        {
          id: 3,
          title: 'Mow the lawn'
        }
      ],
      nextTodoId: 4
    }
  },
  methods: {
    async test () {
      this.back = 'waitting...'
      this.$axios.get('http://127.0.0.1:8000/api/test?text=' + this.text)
        .then((response) => {
          const res = response.data
          if (res['respCode'] === '000000') {
            this.back = res['back']
          } else {
            this.back = '测试失败'
          }
        })
    },
    addNewTodo() {
      this.todos.push({
        id: this.nextTodoId++,
        title: this.newTodoText
      })
      this.newTodoText = ''
    }
  }
}
</script>

<template>
  <div>
    <div>
      <el-input v-model="text" placeholder="请输入"></el-input>
      <el-button @click="test()">测试</el-button>
      <p>{{ back }}</p>
    </div>

    <div id="todo-list-example">
      <form v-on:submit.prevent="addNewTodo">
        <label for="new-todo">Add a todo</label>
        <input
          v-model="newTodoText"
          id="new-todo"
          placeholder="E.g. Feed the cat"
        />
        <button>Add</button>
      </form>
      <ul>
        <todoItem
          v-for="(todo, index) in todos"
          :key="todo.id"
          :title="todo.title"
          @remove="todos.splice(index, 1)"
        ></todoItem>
      </ul>
    </div>
  </div>
</template>

<style scoped>

</style>
