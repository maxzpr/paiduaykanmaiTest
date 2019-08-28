<template>
  <v-container>
    <v-dialog v-model="dialog.open" width="750" max-width="100%" @close="cancleForm">
      <v-card :loading="dialog.loading">
        <v-form v-model="formData.valid" ref="form" @submit.prevent="submitForm()">
          <v-card-title class="headline grey lighten-2" primary-title>{{dialog.mode}}สมาชิก</v-card-title>
          <v-container>
            <v-row>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="formData.first_name"
                  :rules="formValidate.required"
                  label="ชื่อจริง"
                  required
                  validate-on-submit
                  name="firstname"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="formData.last_name"
                  :rules="formValidate.required"
                  label="นามสกุล"
                  required
                  name="lasstname"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="formData.email"
                  :rules="formValidate.email"
                  label="อีเมลล์"
                  required
                  name="email"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-select
                  required
                  :rules="formValidate.required"
                  v-model="formData.gender"
                  :items="['male','female']"
                  label="เพศ"
                  name="gender"
                ></v-select>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model="formData.age"
                  :rules="formValidate.number"
                  label="อายุ"
                  type="number"
                  required
                  name="age"
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>

          <v-divider></v-divider>

          <v-card-actions>
            <div v-if="!!formResult">
              <v-alert
                fullwidth
                type="success"
                variant="dense"
                v-if="formResult==='success'"
              >{{(dialog.mode==='เพิ่ม'?'เพิ่มสมาชิก':'แก้ไขสมาชิก')+'สำเร็จ'}}</v-alert>
              <v-alert
                fullwidth
                type="error"
                variant="dense"
                v-if="formResult==='error'"
              >{{(dialog.mode==='เพิ่ม'?'เพิ่มสมาชิก':'แก้ไขสมาชิก')+'ล้มเหลว'}}</v-alert>
              <v-btn color="warning" text @click="cancleForm()" type="button">
                <v-icon>close</v-icon>ปิด
              </v-btn>
            </div>
            <div v-if="!formResult">
              <v-btn
                color="primary"
                text
                @click="submitForm()"
                type="submit"
                v-if="dialog.mode==='เพิ่ม'"
                :disabled="!formData.valid"
              >
                <v-icon>save</v-icon>บันทึก
              </v-btn>
              <v-btn
                color="success"
                text
                @click="submitForm()"
                type="submit"
                v-if="dialog.mode!=='เพิ่ม'"
                :disabled="!formData.valid"
              >
                <v-icon>edit</v-icon>แก้ไข
              </v-btn>
              <v-btn color="warning" text @click="cancleForm()" type="button">
                <v-icon>close</v-icon>ยกเลิก
              </v-btn>
            </div>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>
    <v-card max-width="100%" class="mx-auto card" min-height="650px">
      <div v-if="!loading">
        <v-card style="margin:15px;padding:15px;">
          <v-container>
            <v-row no-gutters>
              <v-col cols="6" md="3" class="pa-2">
                <v-text-field v-model="searchOption.id" label="ID" type="number" />
              </v-col>
              <v-col cols="6" md="3" class="pa-2">
                <v-text-field v-model="searchOption.first_name" label="ชื่อ" type="text" />
              </v-col>
              <v-col cols="6" md="3" class="pa-2">
                <v-text-field v-model="searchOption.last_name" label="นามสกุล" type="text" />
              </v-col>
              <v-col cols="6" md="3" class="pa-2">
                <v-text-field v-model="searchOption.email" label="อีเมล" type="email" />
              </v-col>
              <v-col cols="6" md="3" class="pa-2">
                <v-text-field v-model.number="searchOption.age" label="อายุ" type="number" />
              </v-col>
              <v-col cols="6" md="3" class="pa-2">
                <v-range-slider
                  class="mt-5"
                  v-model="searchOption.ageRange"
                  step="1"
                  ticks
                  thumb-label="always"
                  label="ช่วงอายุ"
                ></v-range-slider>
              </v-col>
              <v-col cols="12" md="3" class="pa-2">
                <label>เพศ</label>
                <div>
                  <input type="checkbox" v-model="searchOption.gender" value="male" /> male
                  <input type="checkbox" v-model="searchOption.gender" value="female" /> female
                </div>
              </v-col>
              <v-col cols="3" md="3" class="pa-2">
                <v-btn color="warning person_add_btn" @click="search()">
                  <v-icon>search</v-icon>ค้นหา
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
        <v-btn color="primary person_add_btn" @click="toggleFormDialog('เพิ่ม')">
          <v-icon>person_add</v-icon>เพิ่มสมาชิก
        </v-btn>
        <v-data-table
          v-model="selected"
          :loading="tableLoad"
          :headers="headers"
          :items="users"
          class="user-table elevation-2"
          :options.sync="paginations"
          show-select
          loading-text="กำลังโหลด..."
          :rows-per-page="20"
        >
          <template v-slot:item.แก้ไข="{ item }">
            <v-icon class="mr-2" @click="toggleFormDialog('แก้ไข',item)">edit</v-icon>
            <v-icon class="mr-2" @click="del(item)">delete</v-icon>
          </template>
        </v-data-table>
      </div>
      <div class="text-center" v-if="loading">
        <v-progress-circular :size="70" color="green" indeterminate></v-progress-circular>
      </div>
    </v-card>
  </v-container>
</template>

<style scoped>
.v-progress-circular {
  margin: 1rem;
  margin-top: 25% !important;
}

.card {
  margin-top: 1.2em;
  padding-top: 1rem;
}

.user-table {
  margin-top: 25px;
  box-shadow: 0 -5px 5px black;
}

.person_add_btn {
  margin: 1em;
}
</style>

<script>
const api_host = "http://127.0.0.1";

export default {
  data: () => ({
    loading: true,
    headers: [
      { text: "ID", value: "id" },
      { text: "ชื่อ", value: "first_name" },
      { text: "นามสกุล", value: "last_name" },
      { text: "อีเมลล์", value: "email" },
      { text: "เพศ", value: "gender" },
      { text: "อายุ", value: "age" },
      { text: "#", value: "แก้ไข" }
    ],
    users: [],
    selected: [],
    paginations: {
      page: 1,
      itemsPerPage: 20,
      pageStart: 1,
      pageCount: 2,
      itemsLength: 50,
      rowsPerPage: 10
    },
    dialog: {
      open: false,
      loading: false,
      mode: "เพิ่ม"
    },
    formData: {
      valid: false,
      first_name: "",
      last_name: "",
      email: "",
      gender: "",
      age: ""
    },
    formValidate: {
      required: [v => !!v || "กรุณาใส่ข้อมูล"],
      email: [
        v => !!v || "กรุณาใส่อีเมลล์",
        v => /.+@.+/.test(v) || "อีเมลล์ไม่ถูกต้อง"
      ],
      number: [
        v => !!v || "กรุณาใส่ข้อมูล",
        v => (/[0-9]/.test(v) && v >= 1) || "กรุณาใส่ตัวเลขและมากกว่า 0"
      ]
    },
    formResult: false,
    formSuccess: false,
    searchOption: {
      first_name: "",
      last_name: "",
      gender: [],
      age: "",
      email: "",
      id: null,
      ageRange: [0, 200]
    },
    tableLoad: false
  }),
  methods: {
    resetSearch() {
      this.searchOption = {
        first_name: "",
        last_name: "",
        gender: [],
        age: "",
        email: "",
        id: null,
        ageRange: [0, 200]
      };
    },
    async search() {
      let {
        first_name,
        last_name,
        gender,
        age,
        email,
        id,
        ageRange
      } = this.searchOption;
      let whereMap = [];
      this.tableLoad = true;
      if (first_name) whereMap.push(`first_name LIKE '%${first_name}%'`);
      if (last_name) whereMap.push(`last_name LIKE '%${last_name}%'`);
      if (id) whereMap.push(`id = ${id}`);
      if (gender.length > 0)
        whereMap.push(`gender IN ('${gender.join("','")}')`);
      if (age) whereMap.push(`age = ${age}`);
      if (ageRange.length > 0)
        whereMap.push(`age BETWEEN ${ageRange.join(" AND ")}`);
      if (email) whereMap.push(`email LIKE '%${email}%'`);

      let [err, res] = await this.$Sync(
        this.axios.post(`${api_host}/searchUser`, {
          whereMap: whereMap.join(" AND ")
        })
      );

      if (!err && res) {
        let {
          data: { data }
        } = res;
        this.users = [];

        setTimeout(() => {
          this.tableLoad = false;
          this.users = data.map(x => ({
            id: x[0],
            first_name: x[1],
            last_name: x[2],
            email: x[3],
            gender: x[4],
            age: x[5]
          }));
        }, 300);
      }
    },
    async getUsersData() {
      this.tableLoad = true;
      let [err, res] = await this.$Sync(
        this.axios.get(`${api_host}/getUserList`)
      );

      let {
        data: { data }
      } = res;

      if (!err) {
        this.users = data.map(x => ({
          id: x[0],
          first_name: x[1],
          last_name: x[2],
          email: x[3],
          gender: x[4],
          age: x[5]
        }));
        this.tableLoad = false;
        this.loading = false;
      }
    },
    toggleFormDialog(mode = "", val = {}) {
      let User = { ...val };
      this.dialog.mode = mode;
      if (mode === "แก้ไข") {
        this.formData = User;
      }
      this.dialog.open = !this.dialog.open;
    },
    async submitForm() {
      if (this.formData.valid) {
        this.dialog.loading = true;
        let { first_name, last_name, email, gender, age, id } = this.formData;
        let [err, res] = await this.$Sync(
          this.axios.post(
            `${api_host}/${
              this.dialog.mode === "เพิ่ม" ? "createUser" : "editUser"
            }`,
            {
              first_name,
              last_name,
              email,
              gender,
              age,
              id
            }
          )
        );

        if (res && !err) {
          this.formResult = "success";
          this.$refs.form.reset();
          this.getUsersData();
          setTimeout(() => {
            this.dialog.loading = false;
          }, 700);
        } else {
          this.formResult = "error";
        }
      }
    },
    cancleForm() {
      this.dialog = {
        loading: false
      };
      this.formResult = false;
      this.$refs.form.reset();
      setTimeout(() => {
        this.dialog = {
          mode: "เพิ่ม",
          open: false
        };
      }, 500);
    },
    async del(item) {
      if (confirm("ยืนยันการลบ ?")) {
        let { id } = item;
        let [err, res] = await this.$Sync(
          this.axios.post(`${api_host}/delUser`, { id })
        );
        if (!err && res) {
          alert("ลบสำเร็จ");
          this.getUsersData();
        } else {
          alert("ลบล้มเหลว");
        }
      }
    }
  },
  mounted() {
    setTimeout(() => {
      this.getUsersData();
    }, 300);
  }
};
</script>
