import request from '@/utils/request'

export function apiProductList(requestbody) {
  return request({
    url: '/api/product/list',
    method: 'post',
    data: requestbody
  })
}

export function apiProductListAll() {
  return request({
    url: '/api/product/listall',
    method: 'post',
    data: ''
  })
}

export function apiProductCreate(requestbody) {
  return request({
    url: '/api/product/add',
    method: 'post',
    data: requestbody
  })
}

export function apiProductUpdate(requestbody) {
  return request({
    url: '/api/product/update',
    method: 'post',
    data: requestbody
  })
}

export function apiProductDelete(requestbody) {
  return request({
    url: '/api/product/delete',
    method: 'post',
    data: requestbody
  })
}
