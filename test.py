# from clinic.models import Doctor
#
# a = Doctor.objects.get(name="Игнат")
# print(a)


class MaxSumRange:
    def __init__(self, start, end, max_sum):
        self.start = start
        self.end = end
        self.max_sum = max_sum

    def __str__(self):
        return f"Start: {self.start}, end: {self.end}, max_sum: {self.max_sum}"


# def max_subarray(arr):
#     max_sum_range = MaxSumRange(0, 0, 0)
#     start_ind, end_ind = 0, 0
#     curr_sum, max_sum = 0, 0
#     for end_ind in range(len(arr)):
#         curr_sum += arr[end_ind]
#         if curr_sum > max_sum:
#             max_sum = curr_sum
#             max_sum_range.start = start_ind
#             max_sum_range.end = end_ind
#             max_sum_range.max_sum = max_sum
#         elif curr_sum < 0:
#             curr_sum = 0
#             start_ind = end_ind + 1
#             max_sum_range.start = start_ind
#             max_sum_range.end = end_ind
#             max_sum_range.max_sum = max_sum
#     return max_sum_range

def max_subarray(arr):
    max_sum_range = None
    start_ind = 0
    curr_sum = 0
    for end_ind in range(len(arr)):
        if not max_sum_range or curr_sum > max_sum_range.max_sum:
            max_sum_range = MaxSumRange(start_ind, end_ind, curr_sum)
        elif curr_sum < 0:
            curr_sum = 0
            start_ind = end_ind + 1
    return max_sum_range


print(max_subarray([-4, -7, -5, -1, -8, -5]))
