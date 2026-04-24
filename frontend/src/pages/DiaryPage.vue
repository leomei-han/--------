<template>
  <div class="space-y-8">
    <!-- ============ HERO (compact) ============ -->
    <section
      class="relative bg-white rounded-3xl card-elevated overflow-hidden"
    >
      <div class="gradient-blob w-32 h-32 bg-primary-400 -top-12 -left-8" />
      <div
        class="gradient-blob w-28 h-28 bg-accent-400 -bottom-14 -right-8"
        style="animation-delay: -3s"
      />
      <div
        class="relative p-4 lg:p-5 flex flex-col xl:flex-row xl:items-center gap-4"
      >
        <div class="min-w-0 flex-1 flex items-start gap-3">
          <div
            class="w-10 h-10 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 text-white flex items-center justify-center shadow-lg shadow-primary-500/25 flex-shrink-0"
          >
            <svg
              class="w-4.5 h-4.5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25"
              />
            </svg>
          </div>
          <div class="min-w-0 flex-1">
            <span
              class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-primary-50 text-primary-700 text-[10px] font-semibold mb-1.5 tracking-wider uppercase"
              >Travel Journal</span
            >
            <h1
              class="text-lg lg:text-xl font-bold text-gray-900 leading-tight"
            >
              把旅途的每一刻，写进属于你的<span
                class="bg-gradient-to-r from-primary-600 to-accent-500 bg-clip-text text-transparent"
                >城市日记</span
              >
            </h1>
            <p class="mt-1.5 text-sm text-gray-500 leading-relaxed">
              发布后你的推荐会出现在广场，评分、浏览、收藏都会同步保留。
            </p>
          </div>
        </div>
        <div class="flex flex-wrap gap-2 flex-shrink-0 text-xs">
          <span
            class="inline-flex items-center gap-2 rounded-2xl bg-gray-50 px-3 py-2 shadow-md shadow-gray-200/50"
          >
            <span class="text-[11px] text-gray-500">广场日记</span>
            <span class="text-sm font-bold text-primary-700">{{
              diaries.length
            }}</span>
          </span>
          <span
            class="inline-flex items-center gap-2 rounded-2xl bg-gray-50 px-3 py-2 shadow-md shadow-gray-200/50"
          >
            <span class="text-[11px] text-gray-500">累计阅读</span>
            <span class="text-sm font-bold text-accent-600">{{
              totalViews.toLocaleString()
            }}</span>
          </span>
          <span
            class="inline-flex items-center gap-2 rounded-2xl bg-gray-50 px-3 py-2 shadow-md shadow-gray-200/50"
          >
            <span class="text-[11px] text-gray-500">平均评分</span>
            <span class="text-sm font-bold text-gray-900">{{
              averageRating
            }}</span>
          </span>
        </div>
        <div class="flex flex-wrap items-center gap-2 xl:justify-end">
          <button
            v-if="auth.isLoggedIn"
            v-ripple
            class="btn-soft-primary inline-flex items-center gap-2 text-sm"
            @click="toggleComposer"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M19.5 14.25v4.875a1.875 1.875 0 01-1.875 1.875H4.875A1.875 1.875 0 013 19.125V5.625A1.875 1.875 0 014.875 3.75H10.5"
              />
            </svg>
            {{ showComposer ? "收起编辑器" : "写一篇新日记" }}
          </button>
          <button
            v-else
            v-ripple
            class="btn-soft-primary inline-flex items-center gap-2 text-sm"
            @click="auth.openAuthModal('login')"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9"
              />
            </svg>
            登录开始记录
          </button>
          <a
            href="#diary-square"
            class="btn-soft-secondary inline-flex items-center gap-1.5 text-sm"
          >
            浏览广场
            <svg
              class="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3"
              />
            </svg>
          </a>
        </div>
      </div>
    </section>
    <!-- ============ COMPOSER (drawer) ============ -->
    <Transition name="page-fade-slide">
      <section
        v-if="auth.isLoggedIn && showComposer"
        class="bg-white rounded-3xl card-elevated p-6 lg:p-8"
      >
        <div class="flex items-center gap-3 mb-6">
          <div
            class="w-11 h-11 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 text-white flex items-center justify-center shadow-lg shadow-primary-500/25"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931z"
              />
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <h2 class="text-lg font-bold text-gray-900">创作一篇日记</h2>
            <p class="text-xs text-gray-500 mt-0.5">
              以
              <strong class="font-medium text-gray-700">{{
                auth.user?.display_name || "游客"
              }}</strong>
              身份发布，立即出现在广场
            </p>
          </div>
          <button
            type="button"
            class="hidden sm:inline-flex text-xs text-gray-400 hover:text-gray-600 transition-colors"
            @click="showComposer = false"
          >
            收起 ✕
          </button>
        </div>
        <form
          class="grid lg:grid-cols-[1.3fr_1fr] gap-6 lg:gap-8"
          @submit.prevent="publishDiary"
        >
          <!-- Fields -->
          <div class="space-y-5">
            <div>
              <label class="field-label">日记标题</label>
              <input
                v-model="draft.title"
                placeholder="给这次旅程起个名字..."
                maxlength="60"
                class="input-soft text-base font-medium"
              />
            </div>
            <div>
              <label class="field-label">关联目的地（可选）</label>
              <div class="relative">
                <svg
                  class="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z"
                  />
                </svg>
                <select
                  v-model="draft.destination_name"
                  class="input-soft has-leading-icon text-sm text-gray-700 appearance-none"
                >
                  <option value="">不关联</option>
                  <option
                    v-for="item in destinations"
                    :key="item.source_id"
                    :value="item.name"
                  >
                    {{ item.name }} · {{ item.city }}
                  </option>
                </select>
              </div>
            </div>
            <div>
              <label class="field-label">
                <span>正文内容</span>
                <span
                  :class="contentNearLimit ? 'text-amber-600' : 'text-gray-400'"
                  class="normal-case tracking-normal font-medium"
                  >{{ draft.content.length }} / 2000</span
                >
              </label>
              <textarea
                v-model="draft.content"
                placeholder="写下这段旅途中你看到、吃到、感受到的一切…"
                maxlength="2000"
                class="input-soft text-sm min-h-[200px] resize-y leading-relaxed"
              />
            </div>
            <div class="flex flex-wrap items-center gap-3 pt-2">
              <button
                type="submit"
                :disabled="publishing || !canPublish"
                v-ripple
                class="btn-soft-primary inline-flex items-center gap-2 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg
                  v-if="publishing"
                  class="w-4 h-4 animate-spin"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  />
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v8z"
                  />
                </svg>
                <svg
                  v-else
                  class="w-4 h-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M6 12 3.269 3.126A59.768 59.768 0 0 1 21.485 12 59.77 59.77 0 0 1 3.27 20.876L5.999 12Zm0 0h7.5"
                  />
                </svg>
                {{ publishing ? "发布中..." : "发布日记" }}
              </button>
              <button
                type="button"
                class="px-4 py-2.5 text-sm font-medium text-gray-500 hover:text-gray-700 transition-colors"
                @click="resetDraft"
              >
                清空
              </button>
              <p v-if="!canPublish" class="text-xs text-gray-400 sm:ml-auto">
                请填写标题与正文
              </p>
            </div>
          </div>
          <!-- Preview -->
          <div class="space-y-3">
            <p class="field-label !mb-0">封面预览</p>
            <div
              class="relative aspect-[4/5] rounded-2xl overflow-hidden bg-gradient-to-br from-gray-100 to-gray-200 border-0 shadow-md shadow-gray-200/50 shadow-inner"
            >
              <RealImage
                v-if="draftCover"
                :src="draftCover.image_url"
                :name="draftCover.name"
                :city="draftCover.city"
                :latitude="draftCover.latitude"
                :longitude="draftCover.longitude"
                :source-url="draftCover.source_url"
                :alt="draftCover.name"
                class="w-full h-full object-cover"
              />
              <div
                v-else
                class="absolute inset-0 flex flex-col items-center justify-center text-gray-400 p-8 text-center"
              >
                <svg
                  class="w-14 h-14 mb-3 opacity-50"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="1.5"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z"
                  />
                </svg>
                <p class="text-xs font-medium">选择关联目的地</p>
                <p class="text-xs mt-0.5">将自动生成精美封面</p>
              </div>
              <div
                v-if="draft.title || draft.content"
                class="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-black/80 via-black/30 to-transparent"
              >
                <p class="text-white text-base font-bold truncate">
                  {{ draft.title || "未命名日记" }}
                </p>
                <p class="text-white/80 text-[11px] mt-1">
                  {{ auth.user?.display_name }} · 刚刚
                </p>
              </div>
            </div>
            <p class="text-[11px] text-gray-400 leading-relaxed">
              Tip · 标题会出现在封面底部，选择目的地后将自动匹配实景图
            </p>
          </div>
        </form>
      </section>
    </Transition>
    <!-- ============ UNAUTH CTA ============ -->
    <section
      v-if="!auth.isLoggedIn"
      class="relative bg-white rounded-2xl border-0 shadow-md shadow-gray-200/50 overflow-hidden card-elevated"
    >
      <div
        class="gradient-blob w-48 h-48 bg-primary-300 -top-10 -right-10 opacity-40"
      />
      <div
        class="relative flex flex-col sm:flex-row items-start sm:items-center gap-4 p-5 lg:p-6"
      >
        <div
          class="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 text-white flex items-center justify-center shadow-lg shadow-primary-500/25 flex-shrink-0"
        >
          <svg
            class="w-6 h-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25"
            />
          </svg>
        </div>
        <div class="min-w-0 flex-1">
          <h3 class="text-base font-bold text-gray-900">
            登录后开启你的城市日记
          </h3>
          <p class="text-sm text-gray-500 mt-0.5">
            3 秒注册本地账号，即可发布日记、评分与收藏。
          </p>
        </div>
        <div class="flex gap-2 flex-shrink-0 w-full sm:w-auto">
          <button
            class="btn-soft-secondary flex-1 sm:flex-none text-sm"
            @click="auth.openAuthModal('register')"
          >
            注册
          </button>
          <button
            class="btn-soft-primary flex-1 sm:flex-none text-sm"
            @click="auth.openAuthModal('login')"
          >
            登录
          </button>
        </div>
      </div>
    </section>
    <!-- ============ ERROR ============ -->
    <div
      v-if="error"
      class="flex items-start gap-3 p-4 rounded-2xl bg-red-50 border-0 shadow-md shadow-gray-200/50"
    >
      <div
        class="w-8 h-8 rounded-2xl bg-red-100 text-red-600 flex items-center justify-center flex-shrink-0"
      >
        <svg
          class="w-4 h-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 9v3.75m0 3.75h.008v.008H12V16.5Zm9-4.5a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"
          />
        </svg>
      </div>
      <div class="flex-1 min-w-0">
        <p class="text-sm font-semibold text-red-700">{{ error }}</p>
        <p class="text-xs text-red-500/80 mt-0.5">
          请确认后端服务已启动，或稍后重试。
        </p>
      </div>
      <button
        class="px-3 py-1.5 text-xs font-medium text-red-600 hover:text-red-700 bg-white border-0 shadow-md shadow-gray-200/50 rounded-2xl hover:bg-red-50 transition-colors whitespace-nowrap"
        @click="reload"
      >
        重新加载
      </button>
    </div>
    <!-- ============ SQUARE ============ -->
    <section
      id="diary-square"
      class="bg-white rounded-3xl card-elevated p-5 lg:p-6"
    >
      <div class="flex flex-wrap items-start justify-between gap-3">
        <div class="flex items-start gap-3">
          <span class="section-accent h-6 mt-1" />
          <div>
            <h2 class="text-xl font-bold text-gray-900">日记广场</h2>
            <p class="text-sm text-gray-500 mt-1">
              来看看别人去了哪里、怎么玩的，也许就是你下一个灵感。
            </p>
          </div>
        </div>
        <div class="chip-tabs">
          <button
            v-for="chip in filterChips"
            :key="chip.value"
            type="button"
            class="chip-tab"
            :class="{ 'is-active': activeChip === chip.value }"
            @click="activeChip = chip.value"
          >
            {{ chip.label }}
          </button>
        </div>
      </div>
      <form
        class="mt-4 flex flex-col sm:flex-row gap-3"
        @submit.prevent="runSearch"
      >
        <div class="relative flex-1 min-w-0">
          <svg
            class="w-4 h-4 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2 pointer-events-none"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
            />
          </svg>
          <input
            v-model="query"
            placeholder="搜索日记标题、正文、目的地..."
            class="input-soft has-leading-icon text-sm"
          />
        </div>
        <button
          type="submit"
          :disabled="searching"
          v-ripple
          class="btn-soft-primary text-sm disabled:opacity-70 sm:w-auto"
        >
          {{ searching ? "搜索中..." : "搜索" }}
        </button>
      </form>
    </section>
    <!-- ============ RESULTS ============ -->
    <div class="grid lg:grid-cols-[1.5fr_1fr] gap-6 items-start">
      <div class="space-y-8">
        <!-- Search results -->
        <section v-if="searchResults.length">
          <div class="flex items-center justify-between mb-4">
            <h3
              class="text-sm font-semibold text-gray-900 flex items-center gap-2"
            >
              <span
                class="w-1.5 h-1.5 rounded-full bg-primary-500 animate-pulse"
              />
              搜索结果
            </h3>
            <span class="text-xs text-gray-400"
              >{{ searchResults.length }} 条</span
            >
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 stagger-children">
            <article
              v-for="item in searchResults"
              :key="`s-${item.id}`"
              v-tilt
              class="group rounded-2xl bg-white overflow-hidden cursor-pointer transition-all duration-300 flex flex-col"
              :class="
                selected?.id === item.id
                  ? 'ring-2 ring-primary-400 shadow-lg shadow-primary-500/15'
                  : 'border-0 shadow-md shadow-gray-200/50 hover:shadow-xl hover:shadow-primary-500/10'
              "
              @click="selectDiary(item)"
            >
              <div
                class="relative h-44 bg-gradient-to-br from-primary-100 to-accent-100 overflow-hidden"
              >
                <RealImage
                  v-if="item.media_urls?.[0]"
                  :src="item.media_urls?.[0]"
                  :alt="item.title"
                  :name="item.title"
                  :city="item.destination_name || ''"
                  class="w-full h-full object-cover group-hover:scale-[1.06] transition-transform duration-500"
                />
                <div
                  v-else
                  class="absolute inset-0 flex items-center justify-center text-primary-300"
                >
                  <svg
                    class="w-14 h-14 opacity-60"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="1.2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25"
                    />
                  </svg>
                </div>
                <span
                  v-if="item.destination_name"
                  class="absolute top-3 left-3 inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-white/90 backdrop-blur-sm text-primary-700 text-[11px] font-semibold shadow-sm"
                >
                  <svg
                    class="w-3 h-3"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z"
                    />
                  </svg>
                  {{ item.destination_name }}
                </span>
              </div>
              <div class="p-4 flex-1 flex flex-col">
                <h4
                  class="font-semibold text-gray-900 text-[15px] leading-snug line-clamp-1"
                >
                  {{ item.title }}
                </h4>
                <p
                  class="text-xs text-gray-500 mt-1.5 leading-relaxed line-clamp-2"
                >
                  {{ item.content }}
                </p>
                <div class="flex items-center gap-2.5 mt-auto pt-4">
                  <div
                    class="w-7 h-7 rounded-full bg-gradient-to-br from-primary-500 to-accent-500 text-white text-[11px] font-bold flex items-center justify-center shadow-sm"
                  >
                    {{ initialOf(item.author_name) }}
                  </div>
                  <p class="text-xs text-gray-600 font-medium truncate">
                    {{ item.author_name }}
                  </p>
                  <span
                    class="ml-auto flex items-center gap-3 text-[11px] text-gray-500"
                  >
                    <span class="inline-flex items-center gap-1">
                      <svg
                        class="w-3.5 h-3.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                        />
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                        />
                      </svg>
                      {{ item.views ?? 0 }}
                    </span>
                    <span class="inline-flex items-center gap-1">
                      <svg
                        class="w-3.5 h-3.5 text-amber-400 fill-amber-400"
                        viewBox="0 0 24 24"
                      >
                        <path
                          d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z"
                        />
                      </svg>
                      {{ (item.rating ?? 0).toFixed(1) }}
                    </span>
                  </span>
                </div>
              </div>
            </article>
          </div>
        </section>
        <!-- Recommended -->
        <section v-if="sortedDiaries.length">
          <div class="flex items-center justify-between mb-4">
            <h3
              class="text-sm font-semibold text-gray-900 flex items-center gap-2"
            >
              <span class="w-1.5 h-1.5 rounded-full bg-accent-500" />
              {{ searchResults.length ? "更多推荐" : sortLabel }}
            </h3>
            <span class="text-xs text-gray-400"
              >{{ sortedDiaries.length }} 条</span
            >
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 stagger-children">
            <article
              v-for="item in sortedDiaries"
              :key="`r-${item.id}`"
              v-tilt
              class="group rounded-2xl bg-white overflow-hidden cursor-pointer transition-all duration-300 flex flex-col"
              :class="
                selected?.id === item.id
                  ? 'ring-2 ring-primary-400 shadow-lg shadow-primary-500/15'
                  : 'border-0 shadow-md shadow-gray-200/50 hover:shadow-xl hover:shadow-primary-500/10'
              "
              @click="selectDiary(item)"
            >
              <div
                class="relative h-44 bg-gradient-to-br from-primary-100 to-accent-100 overflow-hidden"
              >
                <RealImage
                  v-if="item.media_urls?.[0]"
                  :src="item.media_urls?.[0]"
                  :alt="item.title"
                  :name="item.title"
                  :city="item.destination_name || ''"
                  class="w-full h-full object-cover group-hover:scale-[1.06] transition-transform duration-500"
                />
                <div
                  v-else
                  class="absolute inset-0 flex items-center justify-center text-primary-300"
                >
                  <svg
                    class="w-14 h-14 opacity-60"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="1.2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25"
                    />
                  </svg>
                </div>
                <span
                  v-if="item.destination_name"
                  class="absolute top-3 left-3 inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-white/90 backdrop-blur-sm text-primary-700 text-[11px] font-semibold shadow-sm"
                >
                  <svg
                    class="w-3 h-3"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z"
                    />
                  </svg>
                  {{ item.destination_name }}
                </span>
              </div>
              <div class="p-4 flex-1 flex flex-col">
                <h4
                  class="font-semibold text-gray-900 text-[15px] leading-snug line-clamp-1"
                >
                  {{ item.title }}
                </h4>
                <p
                  class="text-xs text-gray-500 mt-1.5 leading-relaxed line-clamp-2"
                >
                  {{ item.content }}
                </p>
                <div class="flex items-center gap-2.5 mt-auto pt-4">
                  <div
                    class="w-7 h-7 rounded-full bg-gradient-to-br from-primary-500 to-accent-500 text-white text-[11px] font-bold flex items-center justify-center shadow-sm"
                  >
                    {{ initialOf(item.author_name) }}
                  </div>
                  <p class="text-xs text-gray-600 font-medium truncate">
                    {{ item.author_name }}
                  </p>
                  <span
                    class="ml-auto flex items-center gap-3 text-[11px] text-gray-500"
                  >
                    <span class="inline-flex items-center gap-1">
                      <svg
                        class="w-3.5 h-3.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                        />
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                        />
                      </svg>
                      {{ item.views ?? 0 }}
                    </span>
                    <span class="inline-flex items-center gap-1">
                      <svg
                        class="w-3.5 h-3.5 text-amber-400 fill-amber-400"
                        viewBox="0 0 24 24"
                      >
                        <path
                          d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z"
                        />
                      </svg>
                      {{ (item.rating ?? 0).toFixed(1) }}
                    </span>
                  </span>
                </div>
              </div>
            </article>
          </div>
        </section>
        <!-- Loading -->
        <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <SkeletonCard v-for="n in 4" :key="n" />
        </div>
        <!-- Empty -->
        <EmptyState
          v-if="!loading && !sortedDiaries.length && !searchResults.length"
          title="还没有日记"
          description="去发布第一篇吧，开启你的城市漫游记录。"
        >
          <button
            v-if="auth.isLoggedIn"
            class="btn-soft-primary mt-5 inline-flex items-center gap-2 text-sm"
            @click="
              showComposer = true;
              scrollToTop();
            "
          >
            写一篇新日记
          </button>
          <button
            v-else
            class="btn-soft-primary mt-5 inline-flex items-center gap-2 text-sm"
            @click="auth.openAuthModal('login')"
          >
            登录开始记录
          </button>
        </EmptyState>
      </div>
      <!-- Detail -->
      <aside
        v-if="selected"
        class="bg-white rounded-3xl card-elevated overflow-hidden sticky top-20 self-start"
      >
        <div
          class="relative h-52 bg-gradient-to-br from-primary-100 to-accent-100 overflow-hidden"
        >
          <RealImage
            v-if="selected.media_urls?.[0]"
            :src="selected.media_urls?.[0]"
            :alt="selected.title"
            :name="selected.title"
            :city="selected.destination_name || ''"
            class="w-full h-full object-cover"
          />
          <div
            v-else
            class="absolute inset-0 flex items-center justify-center text-primary-300"
          >
            <svg
              class="w-16 h-16 opacity-60"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="1.2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25"
              />
            </svg>
          </div>
          <div
            class="absolute inset-x-0 bottom-0 p-5 bg-gradient-to-t from-black/80 via-black/30 to-transparent"
          >
            <span
              v-if="selected.destination_name"
              class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-white/90 text-primary-700 text-[11px] font-semibold"
            >
              <svg
                class="w-3 h-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z"
                />
              </svg>
              {{ selected.destination_name }}
            </span>
            <h3 class="text-xl font-bold text-white mt-2 leading-tight">
              {{ selected.title }}
            </h3>
          </div>
        </div>
        <div class="p-5 space-y-5">
          <div class="flex items-center gap-3">
            <div
              class="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-accent-500 text-white flex items-center justify-center text-sm font-bold shadow-md shadow-primary-500/20"
            >
              {{ initialOf(selected.author_name) }}
            </div>
            <div class="min-w-0 flex-1">
              <p class="text-sm font-semibold text-gray-900 truncate">
                {{ selected.author_name }}
              </p>
              <p class="text-[11px] text-gray-400 mt-0.5">
                {{ selected.created_at }}
              </p>
            </div>
            <div class="flex items-center gap-3 text-xs text-gray-500">
              <span class="inline-flex items-center gap-1">
                <svg
                  class="w-4 h-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
                  />
                </svg>
                {{ selected.views ?? 0 }}
              </span>
            </div>
          </div>
          <p class="text-sm text-gray-700 leading-[1.8] whitespace-pre-line">
            {{ selected.content }}
          </p>
          <!-- Star rating widget -->
          <div
            class="p-4 rounded-2xl bg-gradient-to-br from-amber-50 via-white to-primary-50/50 border-0 shadow-md shadow-gray-200/50"
          >
            <div class="flex items-start justify-between gap-3">
              <div>
                <p class="text-xs font-semibold text-gray-700">
                  给这篇日记打分
                </p>
                <p class="text-[11px] text-gray-500 mt-0.5">
                  当前
                  <strong class="text-amber-600">{{
                    (selected.rating ?? 0).toFixed(1)
                  }}</strong>
                  分
                </p>
              </div>
              <div
                class="flex items-center gap-0.5"
                @mouseleave="hoverScore = 0"
              >
                <button
                  v-for="star in 5"
                  :key="star"
                  type="button"
                  class="star-btn p-1"
                  @mouseenter="hoverScore = star"
                  @click="rateDiary(star)"
                >
                  <svg
                    class="w-6 h-6 transition-colors"
                    :class="
                      (hoverScore || Math.round(selected.rating ?? 0)) >= star
                        ? 'text-amber-400 fill-amber-400'
                        : 'text-gray-300 fill-transparent stroke-current stroke-[1.5]'
                    "
                    viewBox="0 0 24 24"
                  >
                    <path
                      d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <!-- Advanced tools -->
          <details
            class="reveal group rounded-2xl border-0 shadow-md shadow-gray-200/50 bg-gray-50/60 overflow-hidden"
          >
            <summary
              class="flex items-center justify-between px-4 py-3 hover:bg-gray-100/60 transition-colors"
            >
              <div class="flex items-center gap-2">
                <svg
                  class="w-4 h-4 text-gray-500"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M6 20.25h12m-7.5-3v3m3-3v3m-10.125-3h17.25c.621 0 1.125-.504 1.125-1.125V4.875c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125Z"
                  />
                </svg>
                <span class="text-xs font-semibold text-gray-700"
                  >Huffman 压缩 / 解压 演示</span
                >
              </div>
              <svg
                class="w-4 h-4 text-gray-400 transition-transform group-open:rotate-180"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="m19.5 8.25-7.5 7.5-7.5-7.5"
                />
              </svg>
            </summary>
            <div class="p-4 space-y-3 border-0 shadow-md shadow-gray-200/50">
              <div class="flex flex-wrap gap-2">
                <button class="btn-soft-chip" @click="compress">
                  压缩正文
                </button>
                <button
                  class="btn-soft-chip"
                  :disabled="!compressionPayload"
                  @click="decompress"
                >
                  解压回放
                </button>
                <button class="btn-soft-chip" @click="addView">+1 浏览</button>
              </div>
              <pre
                v-if="compressionResult"
                class="p-3 rounded-2xl bg-slate-900 text-slate-100 text-[10px] leading-relaxed overflow-auto max-h-44 whitespace-pre-wrap"
                >{{ compressionResult }}</pre
              >
              <pre
                v-if="decompressedContent"
                class="p-3 rounded-2xl bg-emerald-50 border-0 shadow-md shadow-gray-200/50 text-[11px] leading-relaxed overflow-auto max-h-44 whitespace-pre-wrap text-emerald-800"
              >
解压结果:
{{ decompressedContent }}</pre
              >
            </div>
          </details>
        </div>
      </aside>
      <div
        v-else
        class="bg-white rounded-3xl card-elevated p-8 sticky top-20 self-start"
      >
        <div class="flex flex-col items-center text-center">
          <div
            class="w-14 h-14 rounded-2xl bg-gradient-to-br from-primary-100 to-accent-100 text-primary-600 flex items-center justify-center mb-3"
          >
            <svg
              class="w-7 h-7"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="1.5"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25"
              />
            </svg>
          </div>
          <p class="text-sm font-semibold text-gray-900">选择一篇日记</p>
          <p class="text-xs text-gray-500 mt-1">
            在左侧点击任意一篇，查看正文与评分
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { api } from "../api/client";
import EmptyState from "../components/EmptyState.vue";
import RealImage from "../components/RealImage.vue";
import SkeletonCard from "../components/SkeletonCard.vue";
import { useAuthStore } from "../stores/auth";
import { useToastStore } from "../stores/toast";
import { useTravelStore } from "../stores/travel";
import { resolveRealMedia } from "../utils/realMedia";
const store = useTravelStore();
const auth = useAuthStore();
const toast = useToastStore();
const diaries = computed(() => store.diaries.items);
const selected = computed(() => store.diaries.selected);
const error = computed(() => store.diaries.error);
const loading = computed(() => store.diaries.loading);
const searchResults = computed(() => store.diarySearchResults.items);
const searching = computed(() => store.diarySearchResults.loading);
const destinations = computed(() => store.destinations.items);
const query = ref("");
const showComposer = ref(false);
const activeChip = ref<"latest" | "hot" | "top">("latest");
const hoverScore = ref(0);
const compressionResult = ref("");
const compressionPayload = ref<{
  encoded: string;
  codes: Record<string, string>;
} | null>(null);
const decompressedContent = ref("");
const publishing = ref(false);
const draft = reactive({
  title: "",
  destination_name: "",
  content: "",
  cover_image_url: "",
});
const filterChips = [
  { value: "latest", label: "最新" },
  { value: "hot", label: "最热" },
  { value: "top", label: "高评分" },
] as const;
const sortLabel = computed(() => {
  if (activeChip.value === "hot") return "最热日记";
  if (activeChip.value === "top") return "高评分日记";
  return "最新日记";
});
const sortedDiaries = computed(() => {
  const list = [...diaries.value];
  if (activeChip.value === "hot") {
    list.sort((a, b) => (b.views ?? 0) - (a.views ?? 0));
  } else if (activeChip.value === "top") {
    list.sort((a, b) => (b.rating ?? 0) - (a.rating ?? 0));
  } else {
    list.sort((a, b) => (b.id ?? 0) - (a.id ?? 0));
  }
  return list;
});
const totalViews = computed(() =>
  diaries.value.reduce((sum, item) => sum + (item.views ?? 0), 0),
);
const averageRating = computed(() => {
  const rated = diaries.value.filter((item) => (item.rating ?? 0) > 0);
  if (!rated.length) return "—";
  const avg =
    rated.reduce((sum, item) => sum + (item.rating ?? 0), 0) / rated.length;
  return avg.toFixed(1);
});
const draftCover = computed(
  () =>
    destinations.value.find((item) => item.name === draft.destination_name) ??
    null,
);
const contentNearLimit = computed(() => draft.content.length >= 1800);
const canPublish = computed(
  () => draft.title.trim().length > 0 && draft.content.trim().length > 0,
);
const initialOf = (name: string | undefined | null) => {
  if (!name) return "旅";
  const trimmed = name.trim();
  return trimmed ? trimmed.slice(0, 1).toUpperCase() : "旅";
};
const toggleComposer = () => {
  showComposer.value = !showComposer.value;
  if (showComposer.value) scrollToTop();
};
const resetDraft = () => {
  draft.title = "";
  draft.content = "";
};
const scrollToTop = () => {
  if (typeof window !== "undefined") {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
};
const selectDiary = (item: any) => store.selectDiary(item);
const runSearch = async () => {
  await store.searchDiaries(query.value);
};
const reload = async () => {
  store.diaries.error = "";
  await store.loadDiaries(true);
};
const compress = async () => {
  if (!selected.value) return;
  const { data } = await api.post("/diaries/compress", {
    content: selected.value.content,
  });
  compressionPayload.value = { encoded: data.encoded, codes: data.codes };
  decompressedContent.value = "";
  compressionResult.value = JSON.stringify(data, null, 2);
};
const decompress = async () => {
  if (!compressionPayload.value) return;
  const { data } = await api.post(
    "/diaries/decompress",
    compressionPayload.value,
  );
  decompressedContent.value = data.content;
};
const addView = async () => {
  if (!selected.value) return;
  await store.selectDiary(selected.value, true);
};
const rateDiary = async (score: number) => {
  if (!selected.value) return;
  if (!auth.isLoggedIn) {
    auth.openAuthModal("login");
    return;
  }
  try {
    await store.rateDiary(selected.value.id, score);
    toast.success(`已评分 ${score} 星`);
  } catch (ratingError: any) {
    store.diaries.error =
      ratingError?.response?.data?.detail || "评分失败，请稍后再试。";
    toast.error("评分失败");
  }
};
const publishDiary = async () => {
  if (!auth.isLoggedIn) {
    auth.openAuthModal("login");
    return;
  }
  if (!canPublish.value) return;
  publishing.value = true;
  try {
    const coverImage = draftCover.value
      ? await resolveRealMedia({
          src: draftCover.value.image_url,
          name: draftCover.value.name,
          city: draftCover.value.city,
          latitude: draftCover.value.latitude,
          longitude: draftCover.value.longitude,
          sourceUrl: draftCover.value.source_url,
          searchHint: draft.destination_name,
        })
      : "";
    await api.post("/diaries", {
      destination_name: draft.destination_name,
      title: draft.title,
      content: draft.content,
      cover_image_url: coverImage || draftCover.value?.image_url,
      media_urls: coverImage
        ? [coverImage]
        : draftCover.value?.image_url
          ? [draftCover.value.image_url]
          : [],
    });
    showComposer.value = false;
    resetDraft();
    await store.loadDiaries(true);
    toast.success("日记发布成功");
  } catch (publishError: any) {
    toast.error(
      publishError?.response?.data?.detail || "发布失败，请稍后再试。",
    );
  } finally {
    publishing.value = false;
  }
};
onMounted(async () => {
  await Promise.all([
    store.loadDiaries(false),
    store.loadFeaturedDestinations(false),
  ]);
  if (!draft.destination_name) {
    draft.destination_name = destinations.value[0]?.name ?? "";
  }
});
</script>
