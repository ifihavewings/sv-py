# Regenerating the PDF file to ensure it's available for download

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Define PDF file path
file_path = "/mnt/data/Vue3_Ref_Unwrapping_Guide.pdf"

# Content for the PDF
content = """
在 Vue 3 中，ref 的解包（unwrapping）机制是为了简化对 ref 值的访问。ref 的值通过 .value 访问，但在某些情况下 Vue 会自动解包，让我们可以直接使用 ref 而不必写 .value。以下是 Vue 3 中所有可能的解包 ref 的规则：

1. 模板中自动解包
在模板中使用 ref，Vue 会自动解包，不需要写 .value。模板中 ref 引用的值直接被解析为普通值。
<template>
  <div>
    <p>计数器：{{ count }}</p> <!-- 直接使用 `count` 而不是 `count.value` -->
    <button @click="count++">增加计数</button>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const count = ref(0);
    return { count };
  }
};
</script>

2. 响应式数据中的嵌套 ref 自动解包
使用 reactive 定义一个对象时，ref 类型的属性会被自动解包。在使用 reactive 的属性时，可以直接使用，不需要 .value。
<template>
  <div>
    <p>用户名：{{ user.name }}</p> <!-- `user.name` 自动解包 -->
    <button @click="user.name = 'Alice'">改名为 Alice</button>
  </div>
</template>

<script>
import { ref, reactive } from 'vue';

export default {
  setup() {
    const name = ref('Bob');
    const user = reactive({
      name // 自动解包为普通属性
    });

    return { user };
  }
};
</script>

3. 组合式 API 返回的 ref 需要 .value 访问
在组合式 API 函数中，返回 ref 类型时不会自动解包。使用时需要显式 .value。
import { ref } from 'vue';

export function useCounter() {
  const count = ref(0);
  const increment = () => {
    count.value++;
  };

  return {
    count,      // 这里返回的是一个 `ref`
    increment
  };
}

在组件中使用 useCounter：
<template>
  <div>
    <p>计数：{{ counter.count }}</p> <!-- 需要使用 .value 或者手动解包 -->
    <button @click="counter.increment">增加</button>
  </div>
</template>

<script>
import { useCounter } from './useCounter';

export default {
  setup() {
    const counter = useCounter();
    return { counter };
  }
};
</script>

4. 在 computed 中自动解包
使用 computed 属性时，如果 computed 依赖的是 ref，会自动解包，不需要 .value。
<template>
  <div>
    <p>总价格：{{ totalPrice }}</p> <!-- totalPrice 自动解包 -->
  </div>
</template>

<script>
import { ref, computed } from 'vue';

export default {
  setup() {
    const price = ref(100);
    const quantity = ref(2);
    const totalPrice = computed(() => price.value * quantity.value); // 自动解包

    return { totalPrice };
  }
};
</script>

5. 在解构 ref 时不会自动解包
在解构 ref 时，Vue 不会自动解包，因此需要手动添加 .value，或者使用 toRefs 包装使之解构后依然保持响应性。
<template>
  <div>
    <p>数量：{{ quantity }}</p>
    <button @click="quantity++">增加</button>
  </div>
</template>

<script>
import { ref, toRefs, reactive } from 'vue';

export default {
  setup() {
    const state = reactive({
      quantity: ref(1)
    });
    const { quantity } = toRefs(state); // 需要 toRefs 保持响应性

    return { quantity };
  }
};
</script>

6. 使用 toRef 解包对象中的单个属性
当需要从响应式对象中单独取出一个属性，并让它依旧是响应式 ref 时，可以使用 toRef。
<template>
  <div>
    <p>状态：{{ name }}</p>
    <button @click="name = 'Alice'">改名为 Alice</button>
  </div>
</template>

<script>
import { reactive, toRef } from 'vue';

export default {
  setup() {
    const state = reactive({
      name: 'Bob',
      age: 25
    });
    const name = toRef(state, 'name'); // 保持响应性

    return { name };
  }
};
</script>

7. 使用 unref 解包
在特定情况下，可以使用 unref 手动解包 ref，返回其值。
import { ref, unref } from 'vue';

export default {
  setup() {
    const count = ref(10);
    const logCount = () => {
      console.log(unref(count)); // 返回解包后的值
    };

    return { logCount };
  }
};

总结：
- 模板中自动解包。
- 响应式对象（reactive）中属性自动解包。
- computed 内自动解包。
- 组合式函数中返回的 ref 需要显式 .value。
- 解构时不会自动解包。
- toRefs 和 toRef 保持属性响应性。
- unref 手动解包。
"""

# Create PDF using reportlab
pdf_canvas = canvas.Canvas(file_path, pagesize=A4)
width, height = A4

# Set font
pdf_canvas.setFont("Helvetica", 10)

# Define line height and starting y position
line_height = 12
y_position = height - 40

# Split content into lines and add to PDF
for line in content.splitlines():
    if y_position < 40:  # Add a new page if space is running out
        pdf_canvas.showPage()
        pdf_canvas.setFont("Helvetica", 10)
        y_position = height - 40

    pdf_canvas.drawString(40, y_position, line)
    y_position -= line_height

# Save the PDF
pdf_canvas.save()

# file_path
