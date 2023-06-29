
import PropTypes from 'prop-types';
import React, { useEffect, useState } from 'react';
import { connect } from 'react-redux';
import { Table, Badge } from 'reactstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faClock } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';

import { Spinner } from 'core';
import {
	fetchProjects,
	getProjects,
	getIsLoading,
	fetchProjectsBypage
} from 'projects/ducks/projects';
import { projectType } from 'projects/propTypes';


const DashboardPage = ({ projects, isLoading, fetchProjectsBypage }) => {

	const [currentpage, SetcurrentPage] = useState(0);

	useEffect(() => {
		fetchProjectsBypage();
	}, [fetchProjectsBypage]);

	if (isLoading) {
		return <Spinner />;
	}


	const Prevresults = (Prevpage) => {
		fetchProjectsBypage(Prevpage);
		SetcurrentPage(currentpage - 1)
	}

	const Nextresults = (Nextpage) => {
		fetchProjectsBypage(Nextpage);
		var url = new URL(Nextpage);
		SetcurrentPage(parseInt(url.searchParams.get('offset')) / 10);

	}

	const calculateProjectHasEnded = project => {
		return ((project.end_date && new Date(project.end_date).getDay()) >= new Date().getDay());
	};

	const ProjectData = projects.results ? projects.results : projects;
	return (
		<>
			<Table striped bordered hover data-testid='table'>
				<thead>
					<tr>
						<th>Project</th>
						<th>Tags</th>
						<th>Company</th> 
						<th>Estimated</th>
						<th>Actual</th>
					</tr>
				</thead>
				<tbody>
					{projects ? ProjectData.map((project, i) => (
						<tr key={project.id}>
							<td data-testid={`project-title-${i}`}>
								<Link to={`/projects/${project.id}`}>
									{calculateProjectHasEnded(project) ? (
										<s>{project.title}</s>
									) : (
										project.title
									)}
								</Link>
								{project.is_over_budget && (
									<Badge
										color="danger"
										className="ml-2"
										data-testid="over-budget-badge"
									>
										<FontAwesomeIcon icon={faClock} />
									</Badge>
								)}
							</td>
							<td data-testid={`project-tags-${i}`}>
								{project.tags.map(tag => (
									<Badge
										key={tag.id}
										color={tag.color}
										className="mr-2"
									>
										{tag.name}
									</Badge>
								))}
							</td>
							<td data-testid={`project-company-name-${i}`}>
								{project.company.name}
							</td>
							<td data-testid={`project-estimated-hours-${i}`}>
								{project.total_estimated_hours}
							</td>
							<td data-testid={`project-actual-hours-${i}`}>
								{project.total_actual_hours}
							</td>
						</tr>
					)) : <tr><td></td><td></td> <td align="center" > End of list..!</td> <td></td><td></td></tr>}
				</tbody>
			</Table>

			<nav aria-label="Page navigation example">
				<ul className="pagination justify-content-center">
					<li className="page-item">
						<button className="page-link" href="#" aria-label="Previous" disabled={!projects.previous}
							onClick={() => { Prevresults(projects.previous) }} >
							<span aria-hidden="true">&laquo;</span>
							<span className="sr-only" >Previous</span>
						</button>
					</li>
					<li className="page-item"><button className="page-link" >{currentpage + 1}</button></li>
					<li className="page-item">
						<button className="page-link" href="#" aria-label="Next" disabled={!projects.next}
							onClick={() => { Nextresults(projects.next) }}>
							<span aria-hidden="true">&raquo;</span>
							<span className="sr-only">Next</span>

						</button>
					</li>
				</ul>
			</nav>
		</>
	);
};

DashboardPage.propTypes = {
	fetchProjects: PropTypes.func.isRequired,
	isLoading: PropTypes.bool.isRequired,
	projects: PropTypes.arrayOf(projectType).isRequired,
};

const mapStateToProps = state => ({
	projects: getProjects(state),
	isLoading: getIsLoading(state),
});

const mapDispatchToProps = dispatch => ({
	fetchProjects: () => dispatch(fetchProjects()),
	fetchProjectsBypage: (pagevalue) => dispatch(fetchProjectsBypage(pagevalue))
});

export default connect(mapStateToProps, mapDispatchToProps)(DashboardPage);
