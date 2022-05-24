import request from '@/utils/request'

export function apiAppList(requestbody) {
  return request({
    url: '/api/app/list',
    method: 'post',
    data: requestbody
  })
}

export function apiAppAdd(requestbody) {
  return request({
    url: '/api/app/add',
    method: 'post',
    data: requestbody
  })
}