<template>
  <tr>
    <td class="fs-content">{{ product.start_day }}</td>
    <td class="fw-bold fs-content">{{ product.bank.name }}</td>
    <td class><RouterLink
          :to="{ name: 'product-detail', params: { category: category, code: product.code}}"
          class="underline-none fs-content"
        >
          {{ product.name }}
        </RouterLink>
    </td>
    <td class="fs-content">{{ option6?.intr_rate }}</td>
    <td class="fs-content">{{ option12?.intr_rate }}</td>
    <td class="fs-content">{{ option24?.intr_rate }}</td> 
    <td class="fs-content">{{ option36?.intr_rate }}</td>
  </tr>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  product: Object,
  category: String
})

const options = ref(props.product.options)
const option6 = options.value.find(v => v.save_term === 6)
const option12 = options.value.find(v => v.save_term === 12)
const option24 = options.value.find(v => v.save_term === 24)
const option36 = options.value.find(v => v.save_term === 36)
</script>

<style scoped>
.fs-content {
  font-size: 0.9rem;
}
.underline-none {
  text-decoration: none;
}
</style>