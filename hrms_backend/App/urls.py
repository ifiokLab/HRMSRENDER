from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('organization/signup/',views.EmployerSignupView.as_view(), name='organization-signup'),
    path('organization/login/',views.EmployerLoginView.as_view(), name='organization-login'),
    path('login/',views.GeneralLoginView.as_view(), name='general-login'),
    path('organization/create/',views.OrganizationCreateView.as_view(), name='organization-create'),
    path('organization/list/',views.EmployerOrganizationsView.as_view(), name='organization-list'),
    path('organization/<int:pk>/edit/', views.OrganizationEditView.as_view(), name='organization-edit'),
    path('organization/<int:pk>/delete/', views.OrganizationDeleteView.as_view(), name='organization-delete'),
    path('invitation/create/',views.InvitationCreateView.as_view(), name='invitation-create'),
    path('client-invitation/',views.ClientInvitationCreateView.as_view(), name='client-invitation'),
    path('departments/list/',views.DepartmentListView.as_view(), name='departments-list'),
    path('register-via-link/<str:invitation_code>/', views.RegisterViaLinkView.as_view(), name='register_via_link'),
    path('organization/<int:Id>/',views.OrganizationDetailView.as_view(), name='organization-detail'),
    path('employees/list/<int:Id>/',views.EmployeeListView.as_view(), name='employee-list'),
    path('membership-department/<int:pk>/change/',views.EmployeeDepartmentChangeView.as_view(), name='membership-department'),
    path('membership-department/<int:pk>/remove/',views.EmployeeRemoveView.as_view(), name='membership-remove'),
    path('off-boarding-list/<int:Id>/',views.EmployeeOffboardingList.as_view(), name='off-boarding-list'),
    path('on-boarding-list/<int:Id>/',views.EmployeeOnboardingList.as_view(), name='on-boarding-list'),

    path('create-time-sheet/',views.CreateTimeSheetAPIView.as_view(), name='create-time-sheet'),
    path('time-sheet/<int:Id>/list/',views.UserTimeSheet.as_view(), name='time-sheet'),
    path('employee/login/',views.EmployeeLoginView.as_view(), name='employee-login'),
    path('employee/organization/list/',views.EmployeeOrganizationsView.as_view(), name='employee-organization-list'),
    path('request/create/',views.CreateRequestView.as_view(), name='request-create'),
    path('request/list/',views.RequestListView.as_view(), name='request-list'),
    path('organization/time-sheet/<int:Id>/list/',views.OrganizationTimeSheet.as_view(), name='time-sheet'),
    path('calculate_salary/<int:user_id>/', views.CalculateSalaryAPIView.as_view(), name='calculate_salary'),
    path('api/submit-payroll/<int:Id>/', views.SubmitPayrollAPIView.as_view(), name='submit-payroll'),
    path('payroll-history/<int:Id>/', views.PayRollHistory.as_view(), name='payroll-history'),
    path('organization/requests/<int:Id>/', views.OrganizationRequestListView.as_view(), name='organization-requests'),

    path('requests-status/', views.RequestStatusView.as_view(), name='requests-status'),
    path('employees-timesheet/<int:Id>/', views.EmployeesTimeSheetList.as_view(), name='employees-timesheet'),
    path('employees-timesheet-status/', views.EmployeesTimesheetStatusView.as_view(), name='employees-timesheet-status'),
    path('staff-timesheet-status/', views.StaffTimesheetStatusView.as_view(), name='staff-timesheet-status'),

    path('instructor/signup/', views.InstructorSignupView.as_view(), name='instructor-signup'),
    path('instructor/login/', views.InstuctorLoginView.as_view(), name='instructor-login'),
    path('instructor/courses/create/', views.InstuctorLoginView.as_view(), name='instructor-login'),

    path('courses/create/', views.CourseCreateView.as_view(), name='create-course'),
    path('api/categories/', views.CategoryListAPIView.as_view(), name='category-list'),
    path('api/subcategories/<int:category_id>/', views.SubCategoryListAPIView.as_view(), name='subcategory-list'),
    path('instructor-courses/', views.InstructorCoursesView.as_view(), name='instructor-courses'),

    path('api/courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/<int:course_id>/add-requirements/', views.RequirementsCreateView.as_view(), name='add-requirements'),
    path('courses/<int:course_id>/add-objectives/', views.ObjectivesCreateView.as_view(), name='add-objectives'),

    path('courses/<int:course_id>/add-section/', views.SectionCreateView.as_view(), name='add-section'),
    path('courses/<int:course_id>/sections/', views.CourseSectionsView.as_view(), name='course-sections'),
    path('sections/<int:section_id>/contents/', views.SectionContentsView.as_view(), name='section-contents'),
    path('api/sections/<int:section_id>/update/', views.UpdateSectionView.as_view(), name='update_section'),
    path('api/sections/<int:section_id>/delete/', views.DeleteSectionView.as_view(), name='delete_section'),
    path('api/sections/<int:courseId>/', views.SectionListView.as_view(), name='section-list'),
    path('api/sections/<int:section_id>/contents/<int:content_id>/update/', views.UpdateContentView.as_view(), name='update-content'),
    path('api/sections/<int:section_id>/contents/<int:content_id>/delete/', views.DeleteContentView.as_view(), name='delete-content'),

    path('courses/<int:course_id>/requirements/<int:requirement_id>/edit/', views.RequirementsUpdateAPIView.as_view(), name='requirements-update'),
    path('courses/<int:course_id>/requirements/<int:requirement_id>/delete/', views.RequirementsDeleteAPIView.as_view(), name='requirements-delete'),
    path('courses/<int:course_id>/objectives/<int:requirement_id>/edit/', views.ObjectivesUpdateAPIView.as_view(), name='objectives-update'),
    path('courses/<int:course_id>/objectives/<int:requirement_id>/delete/', views.ObjectivesDeleteAPIView.as_view(), name='objectives-delete'),
    path('api/course/<int:course_id>/content-type-count/', views.ContentTypeCountView.as_view(), name='content-type-count'),
    path('api/contents/<int:content_id>/', views.ContentDetailView.as_view(), name='content-detail'),
    path('courses/<int:course_id>/edit/', views.EditCourseView.as_view(), name='course-edit'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('api/check-course-owner/<int:courseId>/',views.CheckCourseOwnerView.as_view(),name='check-course-owner'),
    path('api/search-courses/', views.SearchCoursesView.as_view(), name='search-courses'),
    path('api/check-enrollment/<int:course_id>/', views.CheckEnrollmentView.as_view(), name='check-enrollment'),
    path('api/enroll-organization/<int:course_id>/', views.EnrollOrganizationInCourse.as_view(), name='enroll_organization_in_course'),
    path('api/organizations/list/', views.FetchOrganizations.as_view(), name='organizations-list'),
    path('enrolled-courses/', views.EnrolledCoursesView.as_view(), name='enrolled-courses'),

    path('instructor/profile/create/',views.InstructorProfileCreateView.as_view(), name='instructor-profile-create'),
    path('instructor/profile/edit/',views.InstructorProfileEditView.as_view(), name='instructor-profile-edit'),
    path('instructor/profile/fetch/',views.FetchInstructorProfile.as_view(), name='instructor-profile-fetch'),
    path('employee/profile/create/', views.CreateEmployeeProfileAPIView.as_view(), name='create-employee-profile'),
    path('employee/profile/fetch/',views.FetchEmployeeProfile.as_view(), name='employee-profile-fetch'),
    path('employee/profile/edit/',views.EmployeeProfileEditView.as_view(), name='employee-profile-edit'),
    path('client/profile/create/', views.CreateClientProfile.as_view(), name='create-client-profile'),
    path('client/profile/fetch/',views.FetchClientProfile.as_view(), name='client-profile-fetch'),
    path('client/profile/edit/',views.ClientProfileEditView.as_view(), name='client-profile-edit'),

    path('employer/profile/create/', views.CreateEmployerProfileAPIView.as_view(), name='create-employer-profile'),
    path('employer/profile/fetch/',views.FetchEmployerProfile.as_view(), name='employer-profile-fetch'),
    path('employer/profile/edit/',views.EmployerProfileEditView.as_view(), name='employer-profile-edit'),
    path('check-payment-schedule/<int:Id>/',views.CheckPaymentSchedule.as_view(), name='check-payment-schedule'),
    path('set-payment-schedule/',views.SetPaymentSchedule.as_view(), name='set-payment-schedule'),
    path('invoice-list/<int:Id>/', views.InvoiceList.as_view(), name='invoice-list'),
    path('pay-status/', views.PayRollStatusView.as_view(), name='pay-status'),

    path('employee-payroll-history/<int:Id>/', views.EmployeePayRollHistory.as_view(), name='employee-payroll-history'),
    path('api/check-organization-enrollment/<int:course_id>/', views.CheckOrganizationEnrollmentView.as_view(), name='check-organization-enrollment'),
    path('user/profile/fetch/',views.FetchUserProfile.as_view(), name='user-profile-fetch'),
    path('api/organizations/list/course/<int:courseId>/', views.FetchOrganizationsListCourse.as_view(), name='check-list-organization-enrollment'),
    path('client/signup/', views.ClientSignupView.as_view(), name='client-signup'),
    path('fetch/client-invitation/<str:invitation_code>/', views.FetchInvitation.as_view(), name='client-invitation'),
    path('client-invite/accept/', views.AcceptClientInvitation.as_view(), name='client-invite-accept'),
    path('client-organizations/list/', views.ClientOrganizationListView.as_view(), name='client-organizations'),

    path('clients/list/<int:Id>/', views.ClientListView.as_view(), name='clients-list'),
    path('employee-invite/accept/', views.AcceptEmployeeInvitation.as_view(), name='employee-invite-accept'),
    path('fetch/employee-invitation/<str:invitation_code>/', views.FetchEmployeeInvitation.as_view(), name='employee-invitation'),
    path('client-assignment/create/', views.ClientAssignmentCreateView.as_view(), name='client-assignment-create'),
    path('user-timesheet/<int:Id>/detail/', views.UserTimeSheetDetail.as_view(), name='user-timesheet-detail'),
    path('employee-timesheet/<int:Id>/<int:organizationId>/list/', views.EmployeeTimeSheetList.as_view(), name='employee-timesheet-detail'),
    path('clients/staff/<int:Id>/list/',views.ClientStaffsListView.as_view(), name='staff-list'),

    path('client-rate-update/',views.ClientRateUpdate.as_view(), name='client-rate-update'),
    path('organization-rate-update/',views.OrganizationRateUpdate.as_view(), name='organization-rate-update'),
    path('submit-timesheet-approval/<int:Id>/',views.TimesheetApproval.as_view(), name='submit-timesheet-approval'),
    path('user-timesheet-delete/<int:Id>/',views.UserTimesheetDelete.as_view(), name='user-timesheet-delete'),

    path('password/reset/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password/reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),


   
]