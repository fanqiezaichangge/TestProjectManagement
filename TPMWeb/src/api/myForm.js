import request from '@/utils/request'

export function apiFormList(requestbody) {
  return request({
    url: '/api/form/list',
    method: 'post',
    data: requestbody
  })
}

export function apiFormDetail(requestbody) {
  return request({
    url: '/api/form/detail',
    method: 'post',
    data: requestbody
  })
}

export function apiFormAdd(requestbody) {
  return request({
    url: '/api/form/add',
    method: 'post',
    data: requestbody
  })
} 